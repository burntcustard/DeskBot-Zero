
# How to run:
# $ source ~/Documents/tensorflow/bin/activate
# $ cd Documents/DeskBot-Zero/cnn  (currently HAS to be run from here to find the images)
# $ python neural-net.py

# Resources:
# Tutorial NN based off:
# https://www.tensorflow.org/tutorials/layers
# Understanding NNs:
# http://cv-tricks.com/tensorflow-tutorial/training-convolutional-neural-network-for-image-classification/


import tensorflow as tf
Iterator = tf.data.Iterator

import datasets

tf.logging.set_verbosity(tf.logging.INFO)

num_classes = 0


def main(unused_argv):

    # Load training and evaluation datasets
    train_data, test_data, num_classes = datasets.create()
    #print("!Training_data:")
    #print(train_data)

    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="/tmp/deskbot_convnet_model"
    )

    # Set up logging for predictions
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50
    )

    # New dataset based train_input_fn
    def train_input_fn():
        return train_data.make_one_shot_iterator().get_next()

    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=20000,
        hooks=[logging_hook]
    )

    # Evaluate the model and print results
    def test_input_fn():
        return test_data.make_one_shot_iterator().get_next()
    '''
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_imgs},
        y=eval_labels,
        num_epochs=1,
        shuffle=False
    )
    '''

    eval_results = mnist_classifier.evaluate(input_fn=test_input_fn)
    print(eval_results)


def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""

    print("!!!!!!!!!!!!!!!!")
    print("features:")
    print(features)
    '''
    # Input Layer
    input_layer = tf.reshape(
        features[16383],  # 4(batch_size)*128*128-1 = 16384
        # [(Dynamic) batch size, image width, image height, color channels]
        # TODO: Make image width and height dynamic as well (in datasets.py)?
        # TODO: Switch from 1 channel (grayscale) to 3 channel (rgb or bgr)?
        [4, 128, 128, 1]
    )
    '''

    # Convolutional Layer #1
    conv1 = tf.layers.conv2d(
        inputs=features,
        filters=32,      # Number of filters. TODO: Adjust (much larger?)
        kernel_size=25,  # 25x25px filter (could do [w, h] instead).
        padding="same",  # Output should have the same w,h as the input tensor.
        activation=tf.nn.relu
    )
    # Output of conv1 has a shape of [batch_size, 128, 128, 32]
    #  - same w, h as initial image but with 64 channels for the filters.

    # Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(
        inputs=conv1,
        pool_size=8,  # 8x8px pool
        strides=8     # Every 8px (so no overlap)
    )
    # Output of pool1 has a shape of [batch_size, 16, 16, 32]
    #  - 16x16 because 128px (initial size) / 8px (pool size).

    # Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=64,
        kernel_size=25,
        padding="same",
        activation=tf.nn.relu
    )
    # Output of conv2 has a shape of [batch_size, 16, 16, 64]

    # Pooling layer #2
    pool2 = tf.layers.max_pooling2d(
        inputs=conv2,
        pool_size=2,
        strides=2
    )
    # Output of pool2 has a shape of [batch_size, 8, 8, 64]

    # Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 8 * 8 * 64])  # Same as output of pool2
    #  - pool2_flat has shape of [batch_size, (8*8*64=4096)]
    # Connect dense layer with 1024 neurons:
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(
        inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN
    )
    # Output tensor dropout has shape [batch_size, 1024]

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=num_classes)
    # Output shape [batch_size, 20] (provided there are 20 classes)

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step()
        )
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"]
        )
    }
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops
    )


if __name__ == "__main__":
    tf.app.run()

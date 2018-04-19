
# Useful tutorial on tensorflow.contrib.data:
# https://kratzert.github.io/2017/06/15/example-of-tensorflows-new-input-pipeline.html


import glob  # Used to generate image filename list
import tensorflow as tf

num_classes = 0


def input_parser(image_path, label):
    """
    Convert label to one_hot, read image from file & perform adjustments.
    See: https://www.tensorflow.org/api_guides/python/image
    and: https://www.tensorflow.org/programmers_guide/datasets
    """

    image = tf.read_file(image_path)
    image = tf.image.decode_image(image)
    image = tf.reshape(image, [128, 128, 3])
    #image = image[:, :, ::-1]  # BGE -> RGB conversion if needed?
    image = tf.image.rgb_to_grayscale(image)
    #image = tf.image.resize_images(image, [32, 32])
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image, label


def create(training_validation_ratio = 0.6, batch_size = 4):
    """
    Creates and returns a: training dataset, validation dataset, number of classification classes.
    """

    # Get image filenames, labels, and the number of classification classes
    filenames = glob.glob("../img/*.png")
    imgLabels = []
    for filename in filenames:
        imgLabels.append(int(filename.split("-d",1)[1].split('-',1)[0]))
        # Label is currently just the distance integer (int32).
        # Grouping e.g. having a classifier of "distance between 5 and 10cm"
        # will be done here if it's required.
    num_classes = max(imgLabels)

    numTrainImgs = int(len(filenames) * training_validation_ratio)
    training_paths = tf.constant(filenames[:numTrainImgs])
    training_labels = tf.constant(imgLabels[:numTrainImgs])
    evaluation_paths = tf.constant(filenames[numTrainImgs:])
    evaluation_labels = tf.constant(imgLabels[numTrainImgs:])

    # Create TensorFlow Dataset objects
    training_dataset = tf.data.Dataset.from_tensor_slices(
        (training_paths, training_labels)
    )
    training_dataset = training_dataset.map(input_parser)
    training_dataset = training_dataset.batch(batch_size)
    evaluation_dataset = tf.data.Dataset.from_tensor_slices(
        (evaluation_paths, evaluation_labels)
    )
    evaluation_dataset = evaluation_dataset.map(input_parser)
    evaluation_dataset = evaluation_dataset.batch(batch_size)

    return training_dataset, evaluation_dataset, num_classes

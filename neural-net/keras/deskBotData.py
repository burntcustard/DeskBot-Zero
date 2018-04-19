"""
Partly based on the CIFAR10 small images classification dataset code:
https://github.com/keras-team/keras/blob/master/examples/cifar10_cnn.py
"""

import glob  # Used to generate image filename list
import random
import numpy as np
import tensorflow as tf

INITIAL_RES = 128  # Width/height of image files in px
OUTPUT_RES = 32    # Width/height of returned downscaled images in px

sess = tf.InteractiveSession()  # Required for image.eval()


def parse_img(image_path):
    """Load an image from a specific path.
    Returns:
        Numpy array
    """
    image = tf.read_file(image_path)
    image = tf.image.decode_image(image)
    image = tf.reshape(image, [INITIAL_RES, INITIAL_RES, 3])
    image = tf.image.resize_images(image, [OUTPUT_RES, OUTPUT_RES])
    #image = image[:, :, ::-1]  # BGE -> RGB conversion if needed?
    #image = tf.image.rgb_to_grayscale(image)
    #image = tf.image.convert_image_dtype(image, tf.float32)  # In neuralNet.py
    image = image.eval()  # Convert from tensor to Numpy array for Keras
    return image


def load_data(train_test_ratio = 0.6, randomised = True):
    """Loads all images from ../img folder.
    Arguments:
        train_test_ratio -- The amount of data to use as training data [0-1]
        randomised       -- Is the train/test split random or in filename order
    Returns:
        Tuple of Numpy arrays and an int:
        `(training_images, training_labels), (testing_images, testing_labels)`.
    """

    # Get image filenames, labels, and the number of classification classes
    filenames = glob.glob("../img/*.png")
    if randomised:
        random.shuffle(filenames)

    img_labels = []
    for filename in filenames:
        label = int(filename.split("-d",1)[1].split('-',1)[0])
        label = label // 4  # Group into [max] / x catagories
                            # E.g. 4: "distance between 5 and 10cm" = group '1'
                            # E.g. 20 = 5, 13 = 3, 4 = 0.
        img_labels.append(label)
    num_classes = max(img_labels) + 1  # E.g. max label 5 -> 0-5 inclusive
    num_total_samples = len(filenames)
    num_train_samples = int(num_total_samples * train_test_ratio)
    num_test_samples = num_total_samples - num_train_samples

    training_images = np.empty(
        (num_train_samples, OUTPUT_RES, OUTPUT_RES, 3), dtype='uint8'
    )
    training_labels = np.asarray(img_labels[:num_train_samples], dtype='uint8')

    for i in range(0, num_train_samples):
        training_images[i] = parse_img(filenames[i])

    test_images = np.empty(
        (num_test_samples, OUTPUT_RES, OUTPUT_RES, 3), dtype='uint8'
    )
    test_labels = np.asarray(img_labels[num_train_samples:], dtype='uint8')

    for i in range(0, num_test_samples):
        test_images[i] = parse_img(filenames[i + num_train_samples])

    return ((training_images, training_labels),
            (test_images, test_labels),
            num_classes)


import tensorflow as tf


def dataset(sess, next_element, name):
    """
    Prints each element of a dataset until the end is reached.
    !WARNING! With large dataset MANY lines will be printed.
    """

    print(name.capitalize(), "dataset :")
    while True:
        try:
            elem = sess.run(next_element)
            print("  ", elem)
        except tf.errors.OutOfRangeError:
            print("End of", name, "dataset.")
            break

import math
import random

from utils import plotutils

# Maps tuples and their classes
_classes = dict()

# Centroids
_blue_centroid = (0.0, 0.0)
_red_centroid = (0.0, 0.0)


def calculate_euclidian(a, b):
    return math.sqrt(math.pow((b[0] - a[0]), 2) + math.pow((b[1] - a[1]), 2))


def label_element(element):
    """
    Calculates the euclidian distance between the element and the centroid
    and then defines the label by the closest one
    """
    blue_euc = calculate_euclidian(element, _blue_centroid)
    red_euc = calculate_euclidian(element, _red_centroid)

    if blue_euc < red_euc:
        _classes[element] = 'blue'
    else:
        _classes[element] = 'red'


def generate_random_centroids(coords):
    """
    Generates the first random centroids
    """
    global _blue_centroid
    global _red_centroid

    _blue_centroid = random.choice(coords)
    _red_centroid = random.choice(coords)

    while _red_centroid == _blue_centroid:
        _red_centroid = random.choice(coords)


def centroids_changed(blue_temp, red_temp):
    """
    Checks if the centroids have changed
    """
    if blue_temp != _blue_centroid:
        return True
    if red_temp != _red_centroid:
        return True

    return False


def calculate_new_centroid(centroid_elements):
    """
    Updates a specific centroid
    """
    element_count = len(centroid_elements)
    x_sum = 0.0
    y_sum = 0.0

    for element in centroid_elements:
        x_sum += element[0]
        y_sum += element[1]

    centroid = ((x_sum / element_count), (y_sum / element_count))
    return centroid


def update_centroids():
    """
    Updates the centroids according to the means
    """
    global _blue_centroid
    global _red_centroid

    blue_elements = list()
    red_elements = list()

    for element in _classes:
        if _classes[element] == 'blue':
            blue_elements.append(element)
        else:
            red_elements.append(element)

    _blue_centroid = calculate_new_centroid(blue_elements)
    _red_centroid = calculate_new_centroid(red_elements)


def calculate_k_means(coords):
    """
    Calculates the K means, with K fixed as two for this coursework
    """
    print('\n*****  Running k-means algorithm *****\n')
    generate_random_centroids(coords)

    # Temp centroids to check for changes
    blue_temp_centroid = (0.0, 0.0)
    red_temp_centroid = (0.0, 0.0)

    while centroids_changed(blue_temp_centroid, red_temp_centroid):
        # Gets the old values for comparison
        blue_temp_centroid = _blue_centroid
        red_temp_centroid = _red_centroid

        for element in coords:
            label_element(element)

        update_centroids()

    print('Centroids: \n\nBlue: ' + str(_blue_centroid) +
          '\nRed: ' + str(_red_centroid) + '\n')

    plotutils.plot_results_matrix('kmeans', _classes)

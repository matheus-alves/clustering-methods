import numpy as np
from scipy.stats import multivariate_normal

from methods import kmeans
from utils import plotutils

# Maps tuples and their classes
_classes = dict()

# Centroids
_blue_centroid = (0.0, 0.0)
_red_centroid = (0.0, 0.0)

# Covariance matrices
_blue_cov = np.matrix('0.0 0.0; 0.0 0.0')
_red_cov = np.matrix('0.0 0.0; 0.0 0.0')

# Mixing coefficients
_blue_pi = 0.0
_red_pi = 0.0

# Posteriori probabilities
_blue_probs = dict()
_red_probs = dict()

# Number of iterations
MAX_ITERATIONS = 10


def calculate_new_centroid(elements, probs):
    """
    Calculates the new centroid for this iteration
    """
    x_sum = 0.0
    y_sum = 0.0

    for element in elements:
        x_sum += (probs[element] * element[0])
        y_sum += (probs[element] * element[1])

    centroid_sum = ((x_sum / len(elements)), (y_sum / len(elements)))

    return centroid_sum


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

    _blue_centroid = calculate_new_centroid(blue_elements, _blue_probs)
    _red_centroid = calculate_new_centroid(red_elements, _red_probs)


def calculate_covariance_matrix(elements, centroid, probs):
    """
    Calculates the new covariance matrices
    """
    cov_sum = np.matrix('0.0 0.0; 0.0 0.0')

    m = np.matrix([centroid[0], centroid[1]])

    for element in elements:
        x = np.matrix([element[0], element[1]])
        cov_sum += (probs[element] * (np.multiply((x - m), (x - m).T)))

    cov_sum /= len(elements)

    return cov_sum


def update_covariance_matrices():
    """
    Updates the covariance matrices
    """
    global _blue_cov
    global _red_cov

    blue_elements = list()
    red_elements = list()

    for element in _classes:
        if _classes[element] == 'blue':
            blue_elements.append(element)
        else:
            red_elements.append(element)

    _blue_cov = calculate_covariance_matrix(
        blue_elements, _blue_centroid, _blue_probs)
    _red_cov = calculate_covariance_matrix(
        red_elements, _red_centroid, _red_probs)


def update_mixing_coefficients():
    """
    Updates the mixing coefficients
    """
    global _blue_pi
    global _red_pi

    blue_elements = list()
    red_elements = list()

    for element in _classes:
        if _classes[element] == 'blue':
            blue_elements.append(element)
        else:
            red_elements.append(element)

    _blue_pi = float(len(blue_elements)) / \
        (len(blue_elements) + len(red_elements))
    _red_pi = float(len(red_elements)) / \
        (len(blue_elements) + len(red_elements))


def calculate_gaussian_multivariate(element, centroid, cov_matrix):
    """
    Calculates the gaussian for the given element
    """
    x = np.array([element[0], element[1]])
    m = np.array([centroid[0], centroid[1]])

    p = multivariate_normal.pdf(x, mean=m, cov=cov_matrix)

    return p


def update_probs():
    """
    Update the posteriori probabilities (Step E)
    """
    for element in _blue_probs:
        blue_prob = calculate_gaussian_multivariate(
            element, _blue_centroid, _blue_cov)
        red_prob = calculate_gaussian_multivariate(
            element, _red_centroid, _red_cov)

        blue_num = _blue_pi * blue_prob
        red_num = _red_pi * red_prob
        den = blue_num + red_num

        _blue_probs[element] = blue_num / den
        _red_probs[element] = red_num / den


def set_first_probs():
    """
    Sets the first posteriori probabilities using the all or nothing strategy
    """
    for element in _classes:
        if _classes[element] == 'blue':
            _blue_probs[element] = 1.0
            _red_probs[element] = 0.0
        else:
            _blue_probs[element] = 0.0
            _red_probs[element] = 1.0


def update_classification():
    """
    Updates the classification of each element
    """
    for element in _classes:
        if _blue_probs[element] > _red_probs[element]:
            _classes[element] = 'blue'
        else:
            _classes[element] = 'red'


def setup():
    """
    Define the old values, using the kmeans results as a starting point
    """
    global _classes

    global _blue_centroid
    global _red_centroid

    _classes = kmeans._classes
    _blue_centroid = kmeans._blue_centroid
    _red_centroid = kmeans._red_centroid

    set_first_probs()
    update_covariance_matrices()
    update_mixing_coefficients()


def calculate_em(coords, iterations):
    """
    Calculates the Expectation Maximization algorithm,
    it reuses most of the values calculated by kmeans
    """
    print('\n*****  Running EM Algorithm *****\n')

    setup()

    # Sets the number of iterations
    global MAX_ITERATIONS
    if iterations > 0:
        MAX_ITERATIONS = iterations

    print('Number of iterations: ' + str(MAX_ITERATIONS))
    it = 1

    while it != MAX_ITERATIONS:
        update_probs()
        update_centroids()
        update_covariance_matrices()
        update_mixing_coefficients()
        update_classification()

        it += 1

    print('\nCentroids: \n\nBlue: ' + str(_blue_centroid) +
          '\nRed: ' + str(_red_centroid))
    print('\nCovariance Matrices: \n\nBlue: \n' + str(_blue_cov) +
          '\nRed: \n' + str(_red_cov))
    print('\nMixing Coefficients: \n\nBlue: ' + str(_blue_pi) +
          '\nRed: ' + str(_red_pi) + '\n')

    plotutils.plot_results_matrix('em', _classes)

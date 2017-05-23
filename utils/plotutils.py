import matplotlib.pyplot as plt

# General configurations
plt.axis([-2, 12, -4, 8])
plt.grid(True)


def plot_main_matrix(coords):
    """
    Plots the initial matrix for debug purposes
    """
    print('\nGenerating Initial Matrix')

    xs = list()
    ys = list()

    for coord in coords:
        xs.append(coord[0])
        ys.append(coord[1])

    plt.plot(xs, ys, 'bd')
    plt.savefig('original_matrix.png')
    print('Saving file original_matrix.png')


def extract_lists(classes, target):
    """
    Helper method to generate the x and y lists of a target class
    """
    coords = list()
    xs = list()
    ys = list()

    for element in classes:
        if classes[element] == target:
            xs.append(element[0])
            ys.append(element[1])

    coords.append(xs)
    coords.append(ys)
    return coords


def plot_results_matrix(algorithm, classes):
    """
    Plots the algorithm results
    """
    print('Generating result matrix for ' + algorithm)

    blue_coords = extract_lists(classes, 'blue')
    red_coords = extract_lists(classes, 'red')

    plt.plot(blue_coords[0], blue_coords[1], 'bd')
    plt.plot(red_coords[0], red_coords[1], 'rd')

    plt.savefig(algorithm + '.png')
    print('Saving file ' + algorithm + '.png')

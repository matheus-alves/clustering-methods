import sys

from methods import em
from utils import plotutils

from methods import kmeans
from utils import filereader


def main(args=sys.argv):
    if len(args) < 2:
        print('Please inform the data file path')
        sys.exit(1)
    file_path = args[1]

    iterations = 0
    if len(args) > 2:
        iterations = int(args[2])

    coordinates = filereader.read_data(file_path)
    plotutils.plot_main_matrix(coordinates)
    kmeans.calculate_k_means(coordinates)
    em.calculate_em(coordinates, iterations)


if __name__ == "__main__":
    main()

import os


def read_data(file_name):
    print('Reading file ' + file_name)
    coordinates = list()

    with open(os.getcwd() + '/' + file_name) as data_file:
        for line in data_file:
            x = float(line[:8])
            y = float(line[8:])

            coord = (x, y)

            coordinates.append(coord)

    return coordinates

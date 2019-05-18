import numpy as np


# Can rotate a 3x3 array by a given amount
def rotate_array(x, amount):
    # Get a list in order of top-left clockwise
    rotateable_list = [x[0, 0], x[0, 1], x[0, 2], x[1, 2], x[2, 2], x[2, 1], x[2, 0], x[1, 0]]

    # Rotate the list
    for i in range(amount):
        rotateable_list.append(rotateable_list.pop(0))

    reshapeable_list = [rotateable_list[0],
                        rotateable_list[1],
                        rotateable_list[2],
                        rotateable_list[7],
                        rotateable_list[3],
                        rotateable_list[6],
                        rotateable_list[5],
                        rotateable_list[4]]

    reshapeable_list.insert(4, x[1, 1])

    return np.reshape(reshapeable_list, (3, 3))

import cv2
from enum import Enum


class SobelDirection(Enum):
    X = 1
    Y = 2
    XY = 3

    def __str__(self):
        if self == SobelDirection.X:
            return "x"
        elif self == SobelDirection.Y:
            return "y"
        else:
            return "xy"


def sobel_x(params):
    return sobel(params, SobelDirection.X)


def sobel_y(params):
    return sobel(params, SobelDirection.Y)


def sobel_xy(params):
    return sobel(params, SobelDirection.XY)


def sobel(params, direction):
    """
    Performs edge detection based on the Sobel algorithm in the given direction.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = f"edge detection (sobel {str(direction)}-direction)"

    # Check if we really want to process an image or if we just wanted to receive the algorithm name.
    if len(params) == 1:
        return params

    # The params dictionary contains at least the following entries:
    # - algorithm_name (as set before)
    # - frame_prev (some functions may need the previous frame too)
    # - frame_curr (the current frame that most functions will process)

    # The task of this function is to set the entry "frame_result".
    # If some more informations need to be passed to the next call of the same function, they can also be written
    # into the dictionary since they will only be overwritten when the algorithm changes.

    img_grayscale = cv2.cvtColor(params["frame_curr"], cv2.COLOR_RGB2GRAY)
    img_blurred = cv2.GaussianBlur(img_grayscale, (3, 3), 0)
    params["frame_result"] = cv2.Sobel(
        img_blurred,
        ddepth=cv2.CV_8U,
        dx=1 if direction == SobelDirection.X or direction == SobelDirection.XY else 0,
        dy=1 if direction == SobelDirection.Y or direction == SobelDirection.XY else 0,
        ksize=5,
    )

    return params


def canny(params):
    """
    Performs edge detection based on the Canny algorithm.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "edge detection (canny)"

    # Check if we really want to process an image or if we just wanted to receive the algorithm name.
    if len(params) == 1:
        return params

    # The params dictionary contains at least the following entries:
    # - algorithm_name (as set before)
    # - frame_prev (some functions may need the previous frame too)
    # - frame_curr (the current frame that most functions will process)

    # The task of this function is to set the entry "frame_result".
    # If some more informations need to be passed to the next call of the same function, they can also be written
    # into the dictionary since they will only be overwritten when the algorithm changes.

    img_grayscale = cv2.cvtColor(params["frame_curr"], cv2.COLOR_RGB2GRAY)
    img_blurred = cv2.GaussianBlur(img_grayscale, (3, 3), 0)
    params["frame_result"] = cv2.Canny(img_blurred, threshold1=100, threshold2=200)

    return params

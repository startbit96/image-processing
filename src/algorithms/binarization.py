import cv2


def binarize_global_threshold(params):
    """
    Binarize by a global threshold. First, the image will be converted to grayscale and then a threshold will
    be used to create a binary image.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "binarization (global threshold)"

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
    img_blurred = cv2.GaussianBlur(img_grayscale, (5, 5), 0)
    (_, img_binary) = cv2.threshold(img_blurred, 127, 255, cv2.THRESH_BINARY)
    params["frame_result"] = img_binary

    return params


def binarize_adaptive_mean_threshold(params):
    """
    Binarize by a adaptive mean threshold. First, the image will be converted to grayscale and then a threshold will
    be used to create a binary image.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "binarization (adaptive mean threshold)"

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
    img_blurred = cv2.GaussianBlur(img_grayscale, (5, 5), 0)
    img_binary = cv2.adaptiveThreshold(
        img_blurred,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=21,
        C=8,
    )
    params["frame_result"] = img_binary

    return params


def binarize_adaptive_gauss_threshold(params):
    """
    Binarize by a adaptive gauss threshold. First, the image will be converted to grayscale and then a threshold will
    be used to create a binary image.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "binarization (adaptive gauss threshold)"

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
    img_blurred = cv2.GaussianBlur(img_grayscale, (5, 5), 0)
    img_binary = cv2.adaptiveThreshold(
        img_blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=21,
        C=8,
    )
    params["frame_result"] = img_binary

    return params

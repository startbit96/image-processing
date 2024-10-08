import cv2


def harris(params):
    """
    Finds corners based on the harris corner detection algorithm.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "corner detection (harris)"

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

    params["frame_result"] = params["frame_curr"]

    return params

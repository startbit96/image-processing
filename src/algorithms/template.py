import cv2


def template(params):
    """
    This is a template for creating a new algorithm that can be used in the image processor class.
    For demonstration reasons, the input frame will be converted to a grayscale image.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "template"

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

    params["frame_result"] = cv2.cvtColor(params["frame_curr"], cv2.COLOR_RGB2GRAY)

    return params

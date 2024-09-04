import cv2
import numpy as np


def optical_flow(params):
    """
    This function applies the optical flow algorithm to the previous and current frame.
    Within the params dictionary, further informations are written.
    """
    # Add the name of the algorithm to the parameters.
    params["algorithm_name"] = "optical flow"

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

    # params for corner detection
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

    # Parameters for lucas kanade optical flow
    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )

    # Check if this is the first run for this algorithm.
    if "mask" not in params:
        # First run.
        params["mask"] = np.zeros_like(params["frame_curr"])
        params["colors"] = np.random.randint(0, 255, (100, 3))
        # Find corners in the current frame.
        params["p0"] = cv2.goodFeaturesToTrack(
            cv2.cvtColor(params["frame_prev"], cv2.COLOR_RGB2GRAY),
            mask=None,
            maxCorners=100,
            qualityLevel=0.3,
            minDistance=7,
            blockSize=7,
        )
        params["frame_result"] = params["frame_curr"]
    else:
        # This is not the first run, we can run optical flow on it.
        p1, st, err = cv2.calcOpticalFlowPyrLK(
            cv2.cvtColor(params["frame_prev"], cv2.COLOR_RGB2GRAY),
            cv2.cvtColor(params["frame_curr"], cv2.COLOR_RGB2GRAY),
            params["p0"],
            None,
            **lk_params,
        )
        if p1 is not None:
            good_new = p1[st == 1]
            good_old = params["p0"][st == 1]
            # draw the tracks
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                params["mask"] = cv2.line(
                    params["mask"],
                    (int(a), int(b)),
                    (int(c), int(d)),
                    params["colors"][i].tolist(),
                    2,
                )
                params["frame_curr"] = cv2.circle(
                    params["frame_curr"],
                    (int(a), int(b)),
                    5,
                    params["colors"][i].tolist(),
                    -1,
                )
            params["p0"] = good_new.reshape(-1, 1, 2)
        params["frame_result"] = cv2.add(params["frame_curr"], params["mask"])

    return params

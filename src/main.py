from argument_parser import get_args
import cv2

# =========================================================================================
#       PARSE ARGUMENTS / GET SETTINGS
# =========================================================================================

print("main.py", flush=True)
args = get_args()


# =========================================================================================
#       CONSTANTS
# =========================================================================================

CV2_WINDOW_NAME_ORIGINAL = "original camera stream"
CV2_WINDOW_NAME_PROCESSED = "processed camera stream"
# 0 does not work on MacOS (https://github.com/opencv/opencv-python/issues/916)
CV2_VIDEO_CAPTURE_DEVICE_ID = 1

# =========================================================================================
#       IMAGE PROCESSOR
# =========================================================================================


# =========================================================================================
#       CAPTURE CAMERA IMAGES AND PROCESS.
# =========================================================================================

# Initialize the windows and the camera stream.
if not args.hide_original_camera_stream:
    cv2.namedWindow(CV2_WINDOW_NAME_ORIGINAL)
cv2.namedWindow(CV2_WINDOW_NAME_PROCESSED)
video_capture = cv2.VideoCapture(CV2_VIDEO_CAPTURE_DEVICE_ID)

if video_capture.isOpened():
    # Capture the first image.
    ret, frame = video_capture.read()
    while ret:
        # Capture the image.
        ret, frame = video_capture.read()

        #

        # Display the original image.
        if not args.hide_original_camera_stream:
            cv2.imshow(CV2_WINDOW_NAME_ORIGINAL, frame)

        # Wait a little bit and exit on ESC.
        key = cv2.waitKey(10)
        if key == 27 or key == ord("q"):
            # Exit on ESC or q.
            break
else:
    print("Cannot open video stream.")

# Terminate the windows and the camera stream.
if not args.hide_original_camera_stream:
    cv2.destroyWindow(CV2_WINDOW_NAME_ORIGINAL)
cv2.destroyWindow(CV2_WINDOW_NAME_PROCESSED)
video_capture.release()

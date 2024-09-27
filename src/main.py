from algorithms.binarization import (
    binarize_global_threshold,
    binarize_adaptive_mean_threshold,
    binarize_adaptive_gauss_threshold,
)
from algorithms.edge_detection import sobel_x, sobel_y, sobel_xy, canny
from algorithms.grayscale import grayscale
from algorithms.optical_flow import optical_flow
from algorithms.original import original

from argument_parser import get_args
from image_processor import ImageProcessor
import curses
import cv2
import sys


# =========================================================================================
#       CONSTANTS
# =========================================================================================

CV2_WINDOW_NAME_ORIGINAL = "original camera stream"
CV2_WINDOW_NAME_PROCESSED = "processed camera stream"


# =========================================================================================
#       WORKAROUND FOR PRINTING INTO THE CONSOLE WHILE CURSES IS ACTIVE
# =========================================================================================


class StdOutWrapper:
    """
    This code was taken from: https://stackoverflow.com/a/14010948
    """

    text = ""

    def write(self, txt):
        self.text += txt
        self.text = "\n".join(self.text.split("\n")[-30:])

    def get_text(self):
        return "\n".join(self.text.split("\n"))


# =========================================================================================
#       MAIN IMAGE PROCESSING LOOP
# =========================================================================================


def main(stdscr):
    """
    This function creates the needed OpenCV video stream and handles the input and UI
    using curses.
    """
    # Parse the arguments / get the settings.
    args = get_args()

    # Create the image processor and the parameter dictionary.
    image_processor = ImageProcessor(
        [
            original,
            grayscale,
            binarize_global_threshold,
            binarize_adaptive_mean_threshold,
            binarize_adaptive_gauss_threshold,
            sobel_x,
            sobel_y,
            sobel_xy,
            canny,
            optical_flow,
        ],
        args.selected_idx,
        args.print_markdown_table,
    )

    # We will pass the parameters to the image processor. These will contain the current and
    # previous image as well as some other parameters, that may be needed by some functions.
    # Some things that will definitly be contained by the params dictionary:
    # - frame_prev (holding the previous frame)
    # - frame_curr (holding the current frame)
    # - frame_result (holding whatever result frame is obtained by the current algorithm)
    # - algorithm_name (the name of the current algorithm)
    params = dict()

    # Initialize the windows and the camera stream.
    if not args.hide_original_stream:
        cv2.namedWindow(CV2_WINDOW_NAME_ORIGINAL)
    cv2.namedWindow(CV2_WINDOW_NAME_PROCESSED)

    # If a path to a video file is given, use this, otherwise, use the camera.
    video_capture = cv2.VideoCapture(
        args.filename_video if args.filename_video is not None else args.device_id
    )

    if video_capture.isOpened():
        # Create the terminal UI using curses.
        curses.start_color()
        curses.init_pair(
            1, curses.COLOR_BLACK, curses.COLOR_WHITE
        )  # Black text on white background
        curses.init_pair(
            2, curses.COLOR_WHITE, curses.COLOR_BLACK
        )  # White text on black background (for selection)
        # Set the entire background to white
        stdscr.bkgd(" ", curses.color_pair(1))
        stdscr.clear()
        # Turn off cursor blinking
        curses.curs_set(0)
        # Otherwise, opencvs window will not open:
        stdscr.nodelay(1)

        # Capture the first image.
        ret, frame_prev = video_capture.read()
        if not ret:
            print("There was an error capturing the first image.")
        while True:
            # Handle the terminal UI.
            stdscr.clear()

            # Display the list of items
            for idx, algorithm_name in enumerate(image_processor.algorithm_names):
                item = f"{idx:03d}\t{algorithm_name}"
                if idx == image_processor.selected_idx:
                    stdscr.addstr(idx, 0, item, curses.color_pair(2))
                else:
                    stdscr.addstr(idx, 0, item, curses.color_pair(1))

            # Refresh the screen
            stdscr.refresh()

            # Capture the image.
            ret, frame_curr = video_capture.read()
            if not ret and args.filename_video is not None:
                # The video ended. Reload the video.
                video_capture.release()
                video_capture = cv2.VideoCapture(args.filename_video)
                continue
            elif not ret:
                break

            # Update the parameters for the image processor.
            params["frame_prev"] = frame_prev
            params["frame_curr"] = frame_curr

            # Process the image.
            params = image_processor.process(params)

            # Display the original image.
            if not args.hide_original_stream:
                cv2.imshow(CV2_WINDOW_NAME_ORIGINAL, params["frame_curr"])

            # Display the processed image.
            cv2.imshow(CV2_WINDOW_NAME_PROCESSED, params["frame_result"])

            # Update the previous frame.
            frame_prev = frame_curr

            # Wait for user input
            key = stdscr.getch()

            # Handle the arrow keys.
            if key == curses.KEY_UP or key == ord("j"):
                # Drop the params, since they may contain further informations from the previous algorithm.
                params = dict()
                image_processor.next_algorithm()
            elif key == curses.KEY_DOWN or key == ord("k"):
                # Drop the params, since they may contain further informations from the previous algorithm.
                params = dict()
                image_processor.prev_algorithm()
            elif key == ord("r"):
                # Refresh the algorithm. This means, we simply delete all the parameters since they store settings
                # some algorithm may use. We force these algorithms to restart.
                params = dict()
            elif key == ord("q") or key == 27:
                break  # Exit the loop if 'q' or 'ESC' is pressed

            # Use OpenCV's waitKey for timing but not for input.
            cv2.waitKey(50)
    else:
        print("Cannot open video stream.")

    # Terminate the windows and the camera stream.
    if not args.hide_original_stream:
        cv2.destroyWindow(CV2_WINDOW_NAME_ORIGINAL)
    cv2.destroyWindow(CV2_WINDOW_NAME_PROCESSED)
    video_capture.release()


# =========================================================================================
#       MAIN
# =========================================================================================

if __name__ == "__main__":
    # To be able to print into the normal console, we need a workaround because otherwise
    # we will see nothing, when curses ends.
    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    # To still be able to see all the error messages, we need to put the main function
    # into a try statement, so we will reach the mystdout print at the end of this section.
    try:
        curses.wrapper(main)
    except:
        pass

    # Now print everything we captured in mystdout to the console.
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())

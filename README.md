# image-processing
Implementation of some OpenCV-functions for testing purposes.

## Usage

```bash
python src/main.py
```

### Dependencies

* [OpenCV](https://pypi.org/project/opencv-python/)

### Command line arguments

| flag | name | description | default |
| :---: | :--- | :--- | :--- |
| `-h` | `--help` | show this help message and exit | `None` |
| `-i` | `--selected-idx` | the index of the algorithm selected when starting the program | `0` |
| `-d` | `--device-id` | the id of the camera that shall be used (if you want to use a video, see the '-f' argument) | `1` |
| `-f` | `--filename-video` | path to the video that shall be processed (if not set, the camera stream will be used) | `None` |
|  | `--hide-original-stream` | hide the original camera / video stream and only show the processed stream | `False` |
|  | `--print-markdown-table` | if set, a markdown table with the available algorithms is printed for easy copy paste into the README | `False` |

### Key bindings

| key | usage |
| :---: | :--- |
| `UP` or `j` | select the previous algorithm |
| `DOWN` or `k` | select the next algorithm |
| `r` | restart the currently selected algorithm |
| `q` or `ESC` | quit the program |

### Available algorithms

| ID | algorithm |
| :---: | :--- |
| `0` | original |
| `1` | grayscale |
| `2` | binarization (global threshold) |
| `3` | binarization (adaptive mean threshold) |
| `4` | binarization (adaptive gauss threshold) |
| `5` | edge detection (sobel x-direction) |
| `6` | edge detection (sobel y-direction) |
| `7` | edge detection (sobel xy-direction) |
| `8` | edge detection (canny) |
| `9` | optical flow |

## Adding new algorithms.

Use the template in `src/algorithms/original.py`. 

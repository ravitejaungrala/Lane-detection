import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

import numpy as np
import matplotlib.image as mpimg
import cv2
from docopt import docopt
from IPython.display import HTML, display
from IPython.core.display import Video
from moviepy.editor import VideoFileClip
from CameraCalibration import CameraCalibration
from Thresholding import *
from PerspectiveTransformation import *
from LaneLines import *


class FindLaneLines:
    def __init__(self):
        """ Init Application"""
        self.calibration = CameraCalibration('camera_cal', 9, 6)
        self.thresholding = Thresholding()
        self.transform = PerspectiveTransformation()
        self.lanelines = LaneLines()

    def forward(self, img):
        out_img = np.copy(img)
        img = self.calibration.undistort(img)
        img = self.transform.forward(img)
        img = self.thresholding.forward(img)
        img = self.lanelines.forward(img)
        img = self.transform.backward(img)

        out_img = cv2.addWeighted(out_img, 1, img, 0.6, 0)
        out_img = self.lanelines.plot(out_img)
        return out_img

    def process_image(self, input_path, output_path):
        img = mpimg.imread(input_path)
        out_img = self.forward(img)
        mpimg.imsave(output_path, out_img)

    def process_video(self, input_path, output_path):
        clip = VideoFileClip(input_path)
        out_clip = clip.fl_image(self.forward)
        out_clip.write_videofile(output_path, audio=False)

        # Display the output video in the notebook
        display(Video(output_path, embed=True))


def main():
    findLaneLines = FindLaneLines()
    findLaneLines.process_video("project_video3.mp4", "output6.mp4")


if __name__ == "__main__":
    main()
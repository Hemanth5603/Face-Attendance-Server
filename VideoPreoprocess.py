#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import face_recognition as fr
import os
import pickle
import numpy as np
import cv2 as cv

class VideoPreprocessor:
    def __init__(self, directory, video_path):
        self.directory = directory
        self.video_path = video_path
        self.fps = None
        self.frame_count = 0
        self.extracted_frame_count = 0

    def empty_folder(self):
        for file in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return True

    def extract_frames_per_second(self):
        try:
            cap = cv.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise IOError("Error opening video!")

            self.fps = cap.get(cv.CAP_PROP_FPS)
            if self.fps <= 0:
                raise ValueError("Invalid FPS value.")

            if self.empty_folder():
                while True:
                    ret, frame = cap.read()

                    if not ret:
                        print("End of video reached.")
                        break

                    # Extract one frame per second
                    if self.frame_count % int(self.fps) == 0:
                        filename = f"{self.directory}/frame_{self.extracted_frame_count}.jpg"
                        cv.imwrite(filename, frame)
                        self.extracted_frame_count += 1

                    self.frame_count += 1

                print(f"Extracted {self.extracted_frame_count} frames to {self.directory}")

        except IOError as e:
            print(f"IOError: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")
        finally:
            cap.release()

# Example usage
'''if __name__ == "__main__":
    directory = "Frames"
    video_path = "video.mp4"

    if not os.path.exists(directory):
        os.makedirs(directory)

    preprocessor = VideoPreprocessor(directory, video_path)
    preprocessor.extract_frames_per_second()'''


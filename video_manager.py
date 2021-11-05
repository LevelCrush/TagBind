import os
import os.path
import glob
import random

class VideoManager:

    def __init__(self, dir):
        self.input_dir = dir
        self.videos = []
        try:
          if not os.path.exists(dir):
            os.makedirs(dir)
        except OSError:
          print('Error: Creating directory: {dir}').format(dir = dir)

        glob_search = "{input}/*.mp4".format(input=dir)
        self.videos = glob.glob(glob_search, recursive=True)
        random.shuffle(self.videos)
        print(self.videos)

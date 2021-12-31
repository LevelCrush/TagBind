import argparse
import os
import os.path
import json
import pathlib

class Configuration:


    def __init__(self):
        # prepare argument parsing

        parser = argparse.ArgumentParser()
        parser.add_argument('input_directory', help='Our initial directory of tags to go through and scan')
        parser.add_argument('output_file', help='The final file destination that we want to render to')
        parser.add_argument('-recurse', help='Scan directories recursively',default=True)
        parser.add_argument('-count', help='The target amount of clips to aim for per video', default=15)
        parser.add_argument('-platform', help='Helps keep track of a specified platform for tags', default='none')
        parser.add_argument('-shuffle', help='Shuffles the clips instead of sorting them alphabetically',
                            default=False)
        parser.add_argument('-allow_repeat', help='Allow resuse of clips', default=True)
        parser.add_argument('-no-database-save', help='Do not save in the database')
        parser.add_argument('-add_banners', help='Toggle Banner text')
        parser.add_argument('-width', help='Width of video', default=1280)
        parser.add_argument('-height', help='Height of video', default=1440)
        parser.add_argument('-fps', help='FPS of the video', default=60)
        parser.add_argument('-vcodec', help='FPS of the video', default="libx264")
        parser.add_argument('-acodec', help='FPS of the video', default="aac")
        parser.add_argument('-transition_duration', help='FPS of the video', default=1)
        parser.add_argument('-volume', help='FPS of the video', default=0.35)
        parser.add_argument('-mute_clips', help='FPS of the video', default=False)
        parser.add_argument('-banners', help='FPS of the video', default=True)
        command_line_arguments = parser.parse_args()
        # parse command line arguments (old code)
        self.platform = command_line_arguments.platform
        self.preset_configs = 'configurations.json'
        if self.platform != 'none':
            self.pull_from_configs(self.platform)
        self.width = int(command_line_arguments.width)
        self.height = int(command_line_arguments.height)
        self.fps = int(command_line_arguments.fps)
        self.clip_count = int(command_line_arguments.count)
        self.input = command_line_arguments.input_directory
        self.output = command_line_arguments.output_file
        self.recurse = command_line_arguments.recurse
        self.shuffle = command_line_arguments.shuffle
        self.repeat = command_line_arguments.allow_repeat
        self.vcodec = command_line_arguments.vcodec
        self.acodec = command_line_arguments.acodec
        self.transition_duration = int(command_line_arguments.transition_duration)
        self.volume = float(command_line_arguments.volume)
        self.mute_clips = command_line_arguments.mute_clips
        self.banners = command_line_arguments.banners
        self.font = command_line_arguments.font_family




        # default paramss





    def pull_from_configs(self, targeted_platform):
        print(targeted_platform)
        with open('configurations.json') as f:
            data = json.load(f)

        print(data)


        for i in data:

            if i == targeted_platform:
                self.width = i[1]
                self.height = i[2]
                self.fps = i[3]
                self.vcodec = i[4]
                self.acodec = i[5]
                self.font = i[6]
                self.mute_clips = i[7]
                self.volume = i[8]
                self.banners = i[9]
                self.transition_duration = i[10]    












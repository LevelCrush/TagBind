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
        parser.add_argument('-recurse', help='Scan directories recursively', action='store_true')
        parser.add_argument('-count', help='The target amount of clips to aim for per video', default=15)
        parser.add_argument('-platform', help='Helps keep track of a specified platform for tags', default='none')
        parser.add_argument('-shuffle', help='Shuffles the clips instead of sorting them alphabetically',
                            action='store_false')
        parser.add_argument('-allow_repeat', help='Allow resuse of clips', action='store_true')
        parser.add_argument('-no-database-save', help='Do not save in the database')
        parser.add_argument('-add_banners', help='Toggle Banner text')
        parser.add_argument('-width', help='Width of video', default=920)
        parser.add_argument('-height', help='Height of video', default=1080)
        parser.add_argument('-fps', help='FPS of the video', default=60)

        command_line_arguments = parser.parse_args()
        # parse command line arguments (old code)
        video_directory = command_line_arguments.input_directory
        output_file = command_line_arguments.output_file
        recurse_directory = command_line_arguments.recurse
        target_tag_count = int(command_line_arguments.count)
        target_platform = command_line_arguments.platform
        shuffle_videos = command_line_arguments.shuffle
        self.preset_configs = 'configurations.json'
        print(target_platform)
        self.width = int(command_line_arguments.width)
        self.height = int(command_line_arguments.height)
        self.fps = int(command_line_arguments.fps)
        self.clip_count = int(command_line_arguments.count)
        self.input = command_line_arguments.input_directory
        self.output = command_line_arguments.output_file
        self.recurse = command_line_arguments.recurse
        self.shuffle = command_line_arguments.shuffle
        self.repeat = command_line_arguments.allow_repeat
        if target_platform != 'none':
            self.pull_from_configs(target_platform)

        # default paramss





    def pull_from_configs(self, targeted_platform):

        with open('configurations.json') as f:
            data = json.load(f)

        print(data)

        for i in data['presets']:
            if i['name'] == targeted_platform:
                self.width = int(i['width'])
                self.height = int(i['height'])
                self.fps = int(i['fps'])







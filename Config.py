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
        parser.add_argument('outro', help='where the outro video file is located')
        parser.add_argument('output_file', help='The final file destination that we want to render to')
        parser.add_argument('-recurse', help='Scan directories recursively',default=True)
        parser.add_argument('-count', help='The target amount of clips to aim for per video', default=15)
        parser.add_argument('-platform', help='Helps keep track of a specified platform for tags', default='none')
        parser.add_argument('-shuffle', help='Shuffles the clips instead of sorting them alphabetically',
                            default=False)
        parser.add_argument('-allow_repeat', help='Allow resuse of clips', default=True)
        parser.add_argument('-no_database_save', help='Do not save in the database')
        parser.add_argument('-add_banners', help='Toggle Banner text')
        parser.add_argument('-width', help='Width of video', default=1280)
        parser.add_argument('-height', help='Height of video', default=1440)
        parser.add_argument('-fps', help='FPS of the video', default=60)
        parser.add_argument('-vcodec', help='the video codec', default="libx264")
        parser.add_argument('-acodec', help='the audio codec', default="aac")
        parser.add_argument('-transition_duration', help='the transition duration', default=1)
        parser.add_argument('-music_volume', help='volume of the video', default=0.35)
        parser.add_argument('-mute_clips', help='mute clip audio', default=False)
        parser.add_argument('-banners', help='enable or disable video banners', default=True)
        parser.add_argument('-font_family', help='determines the banners font', default="Times New Roman")
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
        self.music_volume = float(command_line_arguments.music_volume)
        self.mute_clips = command_line_arguments.mute_clips
        self.banners = command_line_arguments.banners
        self.font = command_line_arguments.font_family
        self.no_database_save = command_line_arguments.no_database_save
        self.outro = command_line_arguments.outro



        # default paramss





    def pull_from_configs(self, targeted_platform):
        with open('configurations.json') as f:
            data = json.load(f)
        for i in data:

            if i == targeted_platform:


                self.width = int(data[targeted_platform]['width'])
                self.height = data[targeted_platform]['height']
                self.fps = data[targeted_platform]['fps']
                self.vcodec = data[targeted_platform]['vcodec']
                self.acodec = data[targeted_platform]['acodec']
                self.clip_count = data[targeted_platform]['clip_count']
                self.font = data[targeted_platform]['font']
                self.mute_clips = data[targeted_platform]['mute_clips']
                self.music_volume = data[targeted_platform]['music_volume']
                self.banners = bool(data[targeted_platform]['banners'])
                self.transition_duration = data[targeted_platform]['transition_duration']












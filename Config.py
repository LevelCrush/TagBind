import argparse
import json
import shlex
import sys


class Configuration:
    def __init__(self):
        # set defaults
        self.outro = ""
        self.clip_count = 15
        self.width = 1280
        self.height = 1440
        self.fps = 60
        self.vcodec = "libx264"
        self.acodec = "aac"
        self.transition_time = 1
        self.music_volume = 0.35
        self.font = "Times New Roman"
        self.mute_clips = False
        self.recurse = False
        self.shuffle = False
        self.repeat = False
        self.no_database_save = False
        self.disabled_banners = False
        self.montage_id = -1

        # check for preset
        parser = argparse.ArgumentParser()
        parser.add_argument("-preset", default="none")
        self.preset = parser.parse_known_args(sys.argv)[0].preset

        # load preset (if exists)
        self._parse_preset()

        # load provide args (not including file name, the first arg)
        args = sys.argv
        del args[0]
        self._parse_args(args)
        print(self.__dict__)

    def _copy_args(self, args):
        if hasattr(args, "input_directory"):
            self.input = args.input_directory
        if hasattr(args, "output_file"):
            self.output = args.output_file
        if hasattr(args, "outro"):
            self.outro = args.outro
        if hasattr(args, "count"):
            self.clip_count = int(args.count)
        if hasattr(args, "preset"):
            self.preset = args.preset
        if hasattr(args, "width"):
            self.width = int(args.width)
        if hasattr(args, "height"):
            self.height = int(args.height)
        if hasattr(args, "fps"):
            self.fps = int(args.fps)
        if hasattr(args, "vcodec"):
            self.vcodec = args.vcodec
        if hasattr(args, "acodec"):
            self.acodec = args.acodec
        if hasattr(args, "transition_time"):
            self.transition_time = float(args.transition_time)
        if hasattr(args, "music_volume"):
            self.music_volume = float(args.music_volume)
        if hasattr(args, "banner_font"):
            self.font = args.banner_font
        if hasattr(args, "mute_clips"):
            self.mute_clips = args.mute_clips
        if hasattr(args, "recurse"):
            self.recurse = args.recurse
        if hasattr(args, "shuffle"):
            self.shuffle = args.shuffle
        if hasattr(args, "allow_repeat"):
            self.repeat = args.allow_repeat
        if hasattr(args, "no_database_save"):
            self.no_database_save = args.no_database_save
        if hasattr(args, "no_banners"):
            self.disabled_banners = args.no_banners
        if hasattr(args, "montage"):
            self.montage_id = int(args.montage)

    def _parse_args(self, input, require_io=True):
        parser = argparse.ArgumentParser()
        if require_io:
            parser.add_argument('input_directory', help='Our initial directory of tags to go through and scan', default=argparse.SUPPRESS)
            parser.add_argument('output_file', help='The final file destination that we want to render to', default=argparse.SUPPRESS)
        parser.add_argument('-outro', help='Add outro clip', default=argparse.SUPPRESS)
        parser.add_argument('-count', help='The target amount of clips to aim for per video', default=argparse.SUPPRESS)
        parser.add_argument('-preset', help='Load specified arguments from configurations.json', default=argparse.SUPPRESS)
        parser.add_argument('-width', help='Width of video in pixels', default=argparse.SUPPRESS)
        parser.add_argument('-height', help='Height of video in pixels', default=argparse.SUPPRESS)
        parser.add_argument('-fps', help='Frame rate the video is encoded at', default=argparse.SUPPRESS)
        parser.add_argument('-vcodec', help='The video codec that is used to encode the output', default=argparse.SUPPRESS)
        parser.add_argument('-acodec', help='The audio codec that is used to encode the output', default=argparse.SUPPRESS)
        parser.add_argument('-transition_time', help='the duration of transitions between clips, minimum is 1', default=argparse.SUPPRESS)
        parser.add_argument('-music_volume', help='Volume for music overlay', default=argparse.SUPPRESS)
        parser.add_argument('-banner_font', help='The font used for banners', default=argparse.SUPPRESS)
        parser.add_argument('--mute_clips', action="store_true", help='Mute clip audio', default=argparse.SUPPRESS)
        parser.add_argument('--recurse', action="store_true", help='Scan input directory recursively' , default=argparse.SUPPRESS)
        parser.add_argument('--shuffle', action="store_true", help='Shuffles the clips instead of sorting them alphabetically', default=argparse.SUPPRESS)
        parser.add_argument('--allow_repeat', action="store_true", help='Allow uses of clips that have been used in previous montages', default=argparse.SUPPRESS)
        parser.add_argument('--no_database_save', action="store_true", help='Do not save montages in the database', default=argparse.SUPPRESS)
        parser.add_argument('--no_banners', action="store_true", help='Disabled banner text', default=argparse.SUPPRESS)
        parser.add_argument('-montage', help='Recreate montage by id, Overrides count, shuffle and allow_repeat arguments', default=argparse.SUPPRESS)
        self._copy_args(parser.parse_args(input))

    def _parse_preset(self):
        if self.preset == "none":
            return

        try:
            with open('configurations.json') as f:
                config_args = json.load(f)[self.preset]
        except KeyError:
            raise LookupError(f"Failed to find preset: '{self.preset}' in configurations.json")

        self._parse_args(shlex.split(config_args), False)
        print(f"Loaded Preset: '{self.preset}' from json")











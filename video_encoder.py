import os
from subprocess import  check_output, CalledProcessError, STDOUT


class VideoEncoder:

    def __init__(self, width = 1920, height = 1080, frame_rate = 30, banners = True, mute_clips = False):
        self._inputs = []
        self._filters = []
        self._input_count = 0
        self._last_video = -1
        self._total_duration = 0
        self._outro = ""
        self._music_count = 0
        self._music_inputs = []

        self.width = width
        self.height = height
        self.fps = frame_rate
        self.enable_banners = banners
        self.mute_clips = mute_clips
        self.music_volume = 0.35
        self.transition_duration = 1

    def _add_wipe(self, video_index, transition_angle=1):
        # Must add a clip before calling this or it will fail
        base_video = f"video{self._last_video}"
        self._last_video += 1
        intermediate_video = f"video{self._last_video}"
        self._last_video += 1
        output_video = f"video{self._last_video}"
        wipe_filter = "[{index}]scale={width}:{height}[input{index}];[input{index}]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/{angle})*H/{duration});if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*{angle}),p(X,Y),0)':enable='lte(t,{duration})',setpts=PTS+{duration}+{offset}/TB[{intermediate}];[{base_video}][{intermediate}]overlay[{output}];".format(
            index=video_index,
            duration=self.transition_duration,
            angle=transition_angle,
            offset=self._total_duration,
            base_video=base_video,
            output=output_video,
            intermediate=intermediate_video,
            width=self.width,
            height=self.height
        )
        self._filters.append(wipe_filter)

    def add_text(self, text, duration=3, delay=1, in_speed=300, out_speed=500):
        # Must add a clip before calling this or it will fail
        base_video = f"video{self._last_video}"
        self._last_video += 1
        output_video = f"video{self._last_video}"
        text_filter = "[{input}]drawtext=fontsize=(h/16):fontfile=./font.ttf:text=\'{text}\':fontcolor=white:box=1:boxcolor=DarkCyan:boxborderw=20:x=if(gt(t\,{end})\,w-text_w-150+((t-{end}) * {ospeed})\,if(gt(w-((t-{start})*{ispeed})\,w-text_w-150)\,w-((t-{start})*{ispeed})\,w-text_w-150)):y=h-text_h-150:enable='between(t,{start},{end} + 3)'[{output}];".format(
            text=text,
            input=base_video,
            output=output_video,
            start=self._total_duration + delay,
            end=self._total_duration + delay + duration,
            ispeed=in_speed,
            ospeed=out_speed
        )
        self._filters.append(text_filter)

    def add_music(self, song_path):
        self._music_count += 1
        self._music_inputs.append(song_path)

    def add_clip(self, video_path, banner=""):
        self._inputs.append(video_path)
        if self._input_count != 0:
            self._add_wipe(self._input_count)
        else:
            self._last_video += 1
            output_video = f"video{self._last_video}"
            scale_filter = "[{input}]scale={width}:{height}[{out}];".format(
                out=output_video,
                input=self._input_count,
                width=self.width,
                height=self.height
            )
            self._filters.append(scale_filter)
        if banner != "" and self.enable_banners:
            self.add_text(banner)
        self._total_duration += self._get_clip_duration(video_path)
        self._input_count += 1

    def add_outro(self, video_path):
        self._outro = video_path

    def create(self, output_path="./out.mp4"):
        outro_length = 0

        if self._outro:
            temp_length = self._total_duration
            self.add_clip(self._outro, "")
            outro_length = self._total_duration - temp_length

        outroless_length = self._total_duration - outro_length
        has_music = self._music_count > 0
        input_arg = ' -i ' + ' -i '.join(map(lambda x: f'"{x}"', self._inputs))
        filter_arg = "".join(self._filters)
        join_args = "-map [video_out]:v"
        audio_args = ""
        audio_sources = []

        if has_music:
            input_arg += ' -i ' + ' -i '.join(map(lambda x: f'"{x}"', self._music_inputs))
            audio_args += ";" + "".join(map(lambda x: f'[{x}:a]', range(self._input_count, self._input_count + self._music_count))) \
               + f"concat=n={self._music_count}:v=0:a=1[music0];[music0]atrim=0:{outroless_length},asetpts=PTS-STARTPTS[music1];[music1]volume=0.5[music2];[music2]afade=t=out:st={outroless_length - 1}:d=1[music_out]"
            audio_sources.append("[music_out]")

        if self.mute_clips and self._outro:
            audio_args += f";[{self._input_count - 1}]adelay={outroless_length * 1000}|{outroless_length * 1000}[outro_out]"
            audio_sources.append("[outro_out]")

        if not self.mute_clips:
            audio_args += ";" + ("".join(map(lambda x: f'[{x}:a]', range(0, self._input_count))))\
                         + f"concat=n={self._input_count}:v=0:a=1[clip_out]"
            audio_sources.append("[clip_out]")

        if audio_sources:
            audio_args += f";{''.join(audio_sources)}amix=inputs={len(audio_sources)}[audio_out]"
            join_args += " -map [audio_out]:a"

        cmd = "\"{cwd}\\ffmpeg\\ffmpeg\" -y {inputs} -filter_complex \"{filter}[video{output_video}]framerate={target_framerate}[video_out]{audio}\" {join} -t {length} {output}".format(
            inputs=input_arg,
            filter=filter_arg,
            output_video=self._last_video,
            target_framerate=self.fps,
            audio=audio_args,
            output=output_path,
            join=join_args,
            length=self._total_duration,
            cwd=os.getcwd()
        )

        print("Creating Video...")
        try:
            ffmpeg_output = check_output(cmd, stderr=STDOUT).decode()
        except CalledProcessError as e:
            print(f"FFmpeg Error: {e.output.decode()}")
            print("Creation Failed!")
            return False

        print("Checking output video")
        output_length = self._get_clip_duration(output_path)
        if abs(self._total_duration - output_length) < 0.5:
            print(f"Video Created: {output_path}")
            return True
        else:
            print(f"Expected Duration: {self._total_duration}s")
            print(f"Found Duration: {output_length}s")
            print(f"Difference: {abs(self._total_duration - output_length)}s")
            print(f"Creation Failed! Maximum difference is 0.5s\n")
            return False

    def get_video_length(self):
        return self._total_duration

    def get_clip_count(self):
        return self._input_count

    @staticmethod
    def _get_clip_duration(filename):
        command = [
            os.getcwd() + '\\ffmpeg\\ffprobe',
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            filename
        ]

        try:
            output = check_output(command, stderr=STDOUT).decode()
        except CalledProcessError as e:
            output = e.output.decode()

        return float(output)

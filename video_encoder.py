import os
from subprocess import  check_output, CalledProcessError, STDOUT


class VideoEncoder:

    def __init__(self, width = 1920, height = 1080, frame_rate = 30, banners = True):
        self._inputs = []
        self._filters = []
        self._input_count = 0
        self._last_video = -1
        self.transition_duration = 1
        self._total_duration = 0
        self.width = width
        self.height = height
        self.fps = frame_rate
        self.enable_banners = banners

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

    def create(self, output_path="./out.mp4"):
        input_arg = ' -i ' + ' -i '.join(map(lambda x: f'"{x}"', self._inputs))
        filter_arg = "".join(self._filters)
        audio_concat = "".join(map(lambda x: f'[{x}:a]', range(0, self._input_count))) + f"concat=n={self._input_count}:v=0:a=1"
        cmd = "ffmpeg -y {inputs} -filter_complex \"{filter}[video{output_video}]framerate={target_framerate};{audio}\" {output}".format(
            inputs=input_arg,
            filter=filter_arg,
            output_video=self._last_video,
            target_framerate=self.fps,
            audio=audio_concat,
            output=output_path
        )
        print(cmd)
        os.system(cmd)

    def get_video_length(self):
        return self._total_duration

    def get_clip_count(self):
        return self._input_count

    @staticmethod
    def _get_clip_duration(filename):
        command = [
            'ffprobe',
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

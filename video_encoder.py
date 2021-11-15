import os
from subprocess import  check_output, CalledProcessError, STDOUT


class VideoEncoder:

    def __init__(self):
        self.inputs = []
        self.filters = []
        self.input_count = 0
        self.last_video = -1
        self.transition_duration = 1
        self.total_duration = 0
        self.width = 1920
        self.height = 1080
        self.fps = 30
        self.enable_banners = True

    def setResolution(self, width, height):
        self.width = width
        self.height = height

    def setFPS(self, fps):
        self.fps = fps

    def setBannersEnabled(self, enabled):
        self.enable_banners = enabled

    def addWipe(self, video_index, transition_angle=1):
        base_video = f"video{self.last_video}"
        self.last_video += 1
        intermediate_video = f"video{self.last_video}"
        self.last_video += 1
        output_video = f"video{self.last_video}"
        filter = "[{index}]scale={width}:{height}[input{index}];[input{index}]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/{angle})*H/{duration});if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*{angle}),p(X,Y),0)':enable='lte(t,{duration})',setpts=PTS+{duration}+{offset}/TB[{intermediate}];[{base_video}][{intermediate}]overlay[{output}];".format(
            index=video_index,
			duration=self.transition_duration,
			angle=transition_angle,
			offset=self.total_duration,
            base_video=base_video,
			output=output_video,
			intermediate=intermediate_video,
			width=self.width,
            height=self.height
		)
        self.filters.append(filter)

    def addText(self, text, duration=3, delay=1, in_speed=30, out_speed=50):
        base_video = f"video{self.last_video}"
        self.last_video += 1
        output_video = f"video{self.last_video}"
        filter = "[{input}]drawtext=fontsize=(h/16):fontfile=./font.ttf:text=\'{text}\':fontcolor=white:box=1:boxcolor=DarkCyan:boxborderw=20:x=if(gt(t\,{end})\,w-text_w-150+((t-{end}) * {ospeed})\,if(gt(w-((t-{start})*{ispeed})\,w-text_w-150)\,w-((t-{start})*{ispeed})\,w-text_w-150)):y=h-text_h-150:enable='between(t,{start},{end} + 3)'[{output}];".format(
            text=text,
			input=base_video,
			output=output_video,
			start=self.total_duration + delay,
            end=self.total_duration + delay + duration,
			ispeed=in_speed,
			ospeed=out_speed
		)
        self.filters.append(filter)

    def addClip(self, video_path, banner=""):
        self.inputs.append(video_path)
        if self.input_count != 0:
            self.addWipe(self.input_count)
        else:
            self.last_video += 1
            output_video = f"video{self.last_video}"
            filter = "[{input}]scale={width}:{height}[{out}];".format(
				out=output_video,
				input=self.input_count,
				width=self.width,
				height=self.height
			)
            self.filters.append(filter)
        if banner != "" and self.enable_banners:
            self.addText(banner)
        self.total_duration += getDuration(video_path)
        self.input_count += 1

    def create(self, output_path="./out.mp4"):
        input_arg = ' -i ' + ' -i '.join(map(lambda x: f'"{x}"', self.inputs))
        filter_arg = "".join(self.filters)
        audio_concat = "".join(map(lambda x: f'[{x}:a]', range(0, self.input_count))) + f"concat=n={self.input_count}:v=0:a=1"
        cmd = os.getcwd() + "\\ffmpeg\\ffmpeg -y {inputs} -filter_complex \"{filter}[video{output_video}]framerate={target_framerate};{audio}\" {output}".format(
            inputs=input_arg,
			filter=filter_arg,
			output_video=self.last_video,
			target_framerate=self.fps,
            audio=audio_concat,
			output=output_path
		)
        print(cmd)
        os.system(cmd)


def getDuration(filename):
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

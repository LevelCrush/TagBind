
# ffmpeg -i old.mp4 -i new.mp4 -filter_complex "[0:v][0:a] [0:v][0:a] [0:v][0:a] [1]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/TN)*H/D);if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*TN),p(X,Y),0)':enable='lte(t,D)',setpts=PTS+D/TB[new];[0:v][new]overlay" wipe.mp4
# ffmpeg -i "./Samples\Destiny 2 2021.10.23 - 16.54.12.02.DVR_Trim.mp4" -i "./Samples\Rocket League 2021.11.03 - 16.24.55.07.DVR_Trim_Trim.mp4" -i "./Samples\Valorant 2021.06.10 - 16.54.02.07.DVR_Trim.mp4" -filter_complex "[1]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/TN)*H/D);if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*TN),p(X,Y),0)':enable='lte(t,D)',setpts=PTS+D/TB[video0];[0:v][video0]overlay" wipe.mp4

import os
from subprocess import  check_output, CalledProcessError, STDOUT

class FFmpeg:
    def __init__(self):
        self.inputs = []
        self.filters = []
        self.input_count = 0
        self.last_video = -1
        self.transition_duration = 1
        self.total_dration = 0

    def addWipe(self, video_index, transition_angle = 1):
        base_video = f"video{self.last_video}"
        self.last_video += 1
        intermediate_video = f"video{self.last_video}"
        self.last_video += 1
        output_video = f"video{self.last_video}"
        filter = "[{index}]scale=1920:1080[input{index}];[input{index}]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/{angle})*H/{duration});if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*{angle}),p(X,Y),0)':enable='lte(t,{duration})',setpts=PTS+{duration}+{offset}/TB[{intermediate}];[{base_video}][{intermediate}]overlay[{output}];".format(index=video_index,duration=self.transition_duration,angle=transition_angle,offset=self.total_dration,base_video=base_video,output=output_video, intermediate=intermediate_video)
        self.filters.append(filter)

    def addText(self, text, duration = 4, delay = 1):
        base_video = f"video{self.last_video}"
        self.last_video += 1
        output_video = f"video{self.last_video}"
        filter = "[{input}]drawtext=fontfile=./font.ttf:text='{text}':fontcolor=white:box=1:boxcolor=DarkCyan@0.75:boxborderw=5:x=w-text_w-200:y=h-text_h-100:enable='between(t,{start},{end})'[{output}];".format(text=text,input=base_video,output=output_video,start=self.total_dration + delay,end=self.total_dration + delay+ duration)
        self.filters.append(filter)

    def addClip(self, video_path):
        self.inputs.append(video_path)
        if self.input_count != 0:
            self.addWipe(self.input_count)
        else:
            self.last_video += 1
            output_video = f"video{self.last_video}"
            filter = "[{input}]scale=1920:1080[{out}];".format(out=output_video,input=self.input_count)
            self.filters.append(filter)
        self.addText(self.input_count)
        self.total_dration += getDuration(video_path)
        print(self.total_dration)
        self.input_count += 1

    def run(self):
        input_arg = ' -i ' + ' -i '.join(map(lambda x: '"{file}"'.format(file = x), self.inputs))
        filter_arg = "".join(self.filters)
        print(self.filters)
        cmd = "ffmpeg -y {inputs} -filter_complex \"{filter}[video{output_video}]framerate={target_framerate}\" out.mp4".format(inputs=input_arg,filter=filter_arg,output_video=self.last_video,target_framerate=30)
        print(cmd)
        os.system(cmd)

def getDuration(filename):

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
        output = check_output( command, stderr=STDOUT ).decode()
    except CalledProcessError as e:
        output = e.output.decode()

    return float(output)

# ffmpeg -i old.mp4 -i new.mp4 -filter_complex "[0:v][0:a] [0:v][0:a] [0:v][0:a] [1]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/TN)*H/D);if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*TN),p(X,Y),0)':enable='lte(t,D)',setpts=PTS+D/TB[new];[0:v][new]overlay" wipe.mp4
# ffmpeg -i "./Samples\Destiny 2 2021.10.23 - 16.54.12.02.DVR_Trim.mp4" -i "./Samples\Rocket League 2021.11.03 - 16.24.55.07.DVR_Trim_Trim.mp4" -i "./Samples\Valorant 2021.06.10 - 16.54.02.07.DVR_Trim.mp4" -filter_complex "[1]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/TN)*H/D);if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*TN),p(X,Y),0)':enable='lte(t,D)',setpts=PTS+D/TB[video0];[0:v][video0]overlay" wipe.mp4

import os

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
        if self.last_video == -1:
            base_video = "0"
        self.last_video += 1
        intermediate_video = f"video{self.last_video}"
        self.last_video += 1
        output_video = f"video{self.last_video}"
        filter = "[{index}]format=yuva444p,geq=lum='p(X,Y)':a='st(1,(1+W/H/{angle})*H/{duration});if(lt(W-X,((ld(1)*T-Y)/(ld(1)*T))*ld(1)*T*{angle}),p(X,Y),0)':enable='lte(t,{duration})',setpts=PTS+{duration}+{offset}/TB[{intermediate}];[{base_video}][{intermediate}]overlay[{output}];".format(index=video_index,duration=self.transition_duration,angle=transition_angle,offset=self.total_dration,base_video=base_video,output=output_video, intermediate=intermediate_video)
        self.filters.append(filter)

    def addClip(self, videoPath):
        self.inputs.append(videoPath)
        if self.input_count != 0:
            self.addWipe(self.input_count)
        self.total_dration += 5
        self.input_count += 1

    def run(self):
        input_arg = ' -i ' + ' -i '.join(map(lambda x: '"{file}"'.format(file = x), self.inputs))
        filter_arg = "".join(self.filters)
        print(self.filters)
        cmd = "ffmpeg -y {inputs} -filter_complex \"{filter}[video{output_video}]framerate={target_framerate}\" out.mp4".format(inputs=input_arg,filter=filter_arg,output_video=self.last_video,target_framerate=30)
        print(cmd)
        os.system(cmd)
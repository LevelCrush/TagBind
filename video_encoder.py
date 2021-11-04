import sys
import os
import os.path
from pprint import pprint



class VideoEncoder:

	# construct our encoder instance
	def __init__(self):
		self.inputs = []
		self.streams = []
		self.input_index = 0
		self.complex_filters = []
		self.encoder_settings = {
			'codec' : 'libx264',
			'preset' : 'veryfast',
			'params' : 'nal-hrd-cbr',
			'b-frames' : 2,
			'bitrate-video-avg' : '10M',
			'bitrate-video-min' : '10M',
			'bitrate-video-max' : '10M',
			'bitrate-video-buffer' : '20M',
			'profile-video' : 'high',
			'level-video' : '4.2'
		}
		self.output_segment = ''


	# add an input into our ffmpeg command
	def input(self, input_file, video_track, audio_track):
		self.inputs.append("\"{file}\"".format(file=input_file))
		self.streams.append("[{index}:v][{index}:a]".format(index = self.input_index, video_track = video_track, audio_track = audio_track))
		self.input_index += 1


	# concat inputs together
	def concat(self, video_label, audio_label):
		complex_filter = "concat=n={total_clips}:v=1:a=1 [{video_label}] [{audio_label}]".format(total_clips = len(self.inputs), video_label = video_label, audio_label = audio_label)
		self.complex_filters.append(complex_filter)

	# adds the scale filter to  our output
	def scale(self, width, height,input_video_label, output_video_label):
		complex_filter = "[{input_video_label}]scale={width}:{height}[{output_video_label}]".format(width = width, height = height, output_video_label = output_video_label, input_video_label = input_video_label)
		self.complex_filters.append(complex_filter)

	# adds the framerate filter to our output
	def framerate(self, target_framerate, input_video_label, output_video_label):
		complex_filter = "[{input_video_label}]framerate={target_framerate}[{output_video_label}]".format(input_video_label = input_video_label, target_framerate = target_framerate, output_video_label = output_video_label)
		self.complex_filters.append(complex_filter)

	# adjust an encoder setting
	def encoder_setting(self, setting, value):
		self.encoder_settings[setting] = value


	def output(self, output_video,output_audio,output_file):
		encoder_string = "-c:v {codec} -preset {preset} -x264-params \"{params}\" -bf {bframes} -b:v {bitrate_avg} -minrate {bitrate_min} -maxrate {bitrate_max} -bufsize {bitrate_buff} -profile:v {profile} -level {level}".format(
			codec = self.encoder_settings['codec'],
			preset = self.encoder_settings['preset'],
			params = self.encoder_settings['params'],
			bframes = self.encoder_settings['b-frames'],
			bitrate_avg = self.encoder_settings['bitrate-video-avg'],
			bitrate_min = self.encoder_settings['bitrate-video-min'],
			bitrate_max = self.encoder_settings['bitrate-video-max'],
			bitrate_buff = self.encoder_settings['bitrate-video-buffer'],
			profile = self.encoder_settings['profile-video'],
			level = self.encoder_settings['level-video']
		)

		self.output_segment = "-map \"[{output_video}]\" -map \"[{output_audio}]\" {encoder_settings}  \"{output_file}\"".format(output_video = output_video, output_audio = output_audio, encoder_settings = encoder_string, output_file = output_file)

	def run(self):

		ffmpeg_inputs = ' -i '.join(self.inputs)
		ffmpeg_streams = ' '.join(self.streams) 
		filter_graphs = '; '.join(self.complex_filters)
		ffmpeg_command = "ffmpeg -i {inputs} -filter_complex \"{audio_video_streams} {filter_graphs}\" {output_string}".format(inputs = ffmpeg_inputs, audio_video_streams = ffmpeg_streams, filter_graphs = filter_graphs, output_string = self.output_segment)
		os.system(ffmpeg_command)

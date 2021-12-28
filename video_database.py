"""
manages the video database configuration
"""
import sqlite3
import glob
import os

class VideoDatabase:

	# constructor for the video database class, just initialize all variables
	def __init__(self, input_dir, recursive=False):
		self._connection = sqlite3.connect('tag.db')
		self._create_db()
		self._input_dir = input_dir
		self._recursive = recursive
		self._current_montage = None
		self._current_montage_id = -1

	def close(self):
		self._connection.close()

	def _create_db(self):
		self._connection.execute('''CREATE TABLE IF NOT EXISTS clips (
										id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
										banner TEXT NULL,
										path TEXT NOT NULL,
										used INTEGER NOT NULL)''')
		self._connection.execute('''CREATE TABLE IF NOT EXISTS montages (
										id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
										clip_count INTEGER NOT NULL,
										path TEXT NOT NULL)''')
		self._connection.execute('''CREATE TABLE IF NOT EXISTS montage_clips (
										montageId INTEGER NOT NULL,
										clipId INTEGER NOT NULL,
										PRIMARY KEY (montageId, clipId),
										FOREIGN KEY(montageId) REFERENCES montages(id),
										FOREIGN KEY(clipId) REFERENCES clips(id))''')
		self._connection.commit()

	def scan_clips(self):
		if self._recursive:
			print("Scanning recursively for clips")
		else:
			print("Scanning for clips")
		video_files = glob.glob(f"{self._input_dir}/*.mp4", recursive=self._recursive)
		cursor = self._connection.cursor()
		for file in video_files:
			cursor.execute(f"SELECT * FROM clips WHERE path = '{file}'")
			res = cursor.fetchall()
			if len(res) == 0:
				print(f"New Clip Found: {file}")
				print("Enter Clip Banner Text:")
				banner = input("Enter your value: ")
				self._cursor.execute(f"INSERT INTO clips (banner,path,used) VALUES ('{banner}','{file}',0)")

		cursor.commit()

	def get_montage_clips(self, montage_id):
		self._current_montage = []
		self._current_montage_id = montage_id
		cursor = self._connection.cursor()
		cursor.execute(f"SELECT clipId, clipIndex FROM montage_clips WHERE montageId = {montage_id}")
		clips = sorted(cursor.fetchall(), key=lambda x: x[1])
		for (clipId, index) in clips:
			cursor.execute(f"SELECT [path], [banner] FROM [dbo].[clips] WHERE id = {clipId}")
			clips[index] = cursor.fetchall()[0]

		return clips

	def get_clips(self, count=0, new_clips=False):
		selector = "WHERE 1 = 1"
		if new_clips:
			selector = "WHERE used = 0"
		cursor = self._connection.cursor()
		self._cursor.execute(f"SELECT TOP {count} * FROM [dbo].[clips] {selector} ORDER BY NEWID()")
		self._current_montage = self._cursor.fetchall()
		self._current_montage_id = -1
		print(self._current_montage)
		clips = []
		for clipId, banner, file, used in self._current_montage:
			clips.append((file, banner))
		return clips

	def save_montage(self, output):
		if self._current_montage_id != -1:
			self._cursor.execute(f"INSERT INTO [dbo].[montages] ([clip_count] ,[path]) OUTPUT INSERTED.id VALUES ({len(self._current_montage)}, '{output}')")
			self._current_montage_id = self._cursor.fetchall()[0][0]
			clip_index = 0;
			for clip_id, name, path, used in self._current_montage:
				self._cursor.execute(f"UPDATE [dbo].[clips] SET [used] = 1 WHERE id = {clip_id}")
				self._cursor.execute(f"INSERT INTO [dbo].[montage_clips] ([montageId],[clipId],[clipIndex]) VALUES ({self._current_montage_id}, {clip_id}, {clip_index})")
				clip_index += 1
			self._cursor.commit()
		return self._current_montage_id

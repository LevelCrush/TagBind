"""
manages the video database configuration
"""
import sqlite3
import glob


class VideoDatabase:

	# constructor for the video database class, just initialize all variables
	def __init__(self, input_dir, recursive=False, use_memory_db=False):
		if use_memory_db:
			self._connection = sqlite3.connect(":memory:")
		else:
			self._connection = sqlite3.connect('tag.db')
			print("Loaded Clip Database")
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
										clipIndex INTEGER NOT NULL,
										PRIMARY KEY (montageId, clipId),
										FOREIGN KEY(montageId) REFERENCES montages(id),
										FOREIGN KEY(clipId) REFERENCES clips(id))''')
		self._connection.commit()

	def scan_clips(self):
		if self._recursive:
			print("Scanning recursively for new clips")
		else:
			print("Scanning for new clips")
		video_files = glob.glob(f"{self._input_dir}/*.mp4", recursive=self._recursive)
		cursor = self._connection.cursor()
		for file in video_files:
			cursor.execute(f"SELECT * FROM clips WHERE path = '{file}'")
			res = cursor.fetchall()
			if len(res) == 0:
				print(f"New Clip Found: {file}")
				banner = input("Enter Clip Banner Text: ")
				cursor.execute(f"INSERT INTO clips (banner,path,used) VALUES ('{banner}','{file}',0)")

		self._connection.commit()

	def get_montage_clips(self, montage_id):
		self._current_montage = []
		self._current_montage_id = montage_id
		cursor = self._connection.cursor()
		cursor.execute(f"SELECT clipId, clipIndex FROM montage_clips WHERE montageId = {montage_id}")
		clips = sorted(cursor.fetchall(), key=lambda x: x[1])
		for (clipId, index) in clips:
			cursor.execute(f"SELECT path, banner FROM clips WHERE id = {clipId}")
			clips[index] = cursor.fetchall()[0]

		return clips

	def get_clips(self, count, randomize_clips=True, new_clips=False):
		selector = "WHERE 1 = 1"
		if new_clips:
			selector = "WHERE used = 0"
		cursor = self._connection.cursor()
		if randomize_clips:
			cursor.execute(f"SELECT * FROM clips {selector} ORDER BY RANDOM() LIMIT {count}")
		else:
			cursor.execute(f"SELECT * FROM clips {selector} ORDER BY path DESC LIMIT {count}")
		self._current_montage = cursor.fetchall()
		self._current_montage_id = -1
		clips = []
		for clipId, banner, file, used in self._current_montage:
			clips.append((file, banner))
		return clips

	def save_montage(self, output):
		if self._current_montage_id == -1:
			cursor = self._connection.cursor()
			cursor.execute(f"INSERT INTO montages (clip_count,path) VALUES ({len(self._current_montage)}, '{output}')")
			cursor.execute("SELECT last_insert_rowid();")
			self._current_montage_id = cursor.fetchall()[0][0]
			clip_index = 0
			for clip_id, name, path, used in self._current_montage:
				cursor.execute(f"UPDATE clips SET used = 1 WHERE id = {clip_id}")
				cursor.execute(f"INSERT INTO montage_clips (montageId,clipId,clipIndex) VALUES ({self._current_montage_id}, {clip_id}, {clip_index})")
				clip_index += 1
			self._connection.commit()
		return self._current_montage_id

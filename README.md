# TagBind
## Requirements
 - Python 3.5 or later
 - Unzip all files directly in the ffmpeg directory

## Ez Pz starting guide
- open shell instance 
- basic usage: python tagbind.py {Enter path to clip directory}" "./out.mp4"
- at the end of the the line above you can add as many flags as you would like to the end but only once each
- When given the prompt to enter Clip Banner Text, enter text that you want to show at the start of each clip
- `"./out.mp4"` is the final destination of the clips, this can be changed to another file location on your system

Tagbind also has pre-built video formats built in (youtube, tiktok, twitter and instagram) 

Type: python tagbind.py "(Enter path here)" "./out.mp4" -preset presetname
*replace presetname with one of the four above*

You can also make your own, edit the configurations.json file 
The flags below take priority over these presets

### Examples

- `python tagbind.py "C:\Users\mongoose925\Videos\League of Legends" "./out.mp4" `

-  `python tagbind.py "C:\Users\mongoose925\Videos\League of Legends" "./out.mp4" -width 254 -height 180`

- `python tagbind.py "C:\Users\mongoose925\Videos\League of Legends" "./out.mp4" -preset twitter`

- `python tagbind.py "C:\Users\mongoose925\Videos\Rocket League" "./out.mp4" -count 3 -outro "C:\Users\mongoose925\Videos\Rocket League\Rocket League 2021.11.03 - 16.15.39.06.DVR_Trim_Trim.mp4"`

Mandatory Arguments
input_directory What this does: Our initial directory of tags to go through and scan
output_file What this does: The final file destination that we want to render to

## Flags
**If the flag has 2 dashes (--) it does not need a value (do not add the quotes when adding flags)**


 -  `-outro` What this does: Add outro clip (SEE EXAMPLES)

 - `-count` What this does: The target amount of clips to aim for per video (max amount of clips in one video, you can increase this to add more) 

 - `-preset` What this does: Load specified arguments from configurations.json 

 - `-width` What this does: Width of video in pixels (Default is 1280)

 - `-height` What this does: Height of video in pixels (Default is 1440)

 - `-fps` What this does: Frame rate the video is encoded at (Default is 60)

 - `-transition_time` What this does: the duration of transitions between clips, minimum is 1 (Default is 1 second)

 - `-music` What this does: Add music overlay, provide mp3 paths separated by comma with space (Default is no music)

 - `-music_volume` What this does: Volume for music overlay (Default is 0.35)

 - `-banner_font` What this does: The font used for banners (Default is Times New Roman)

 - `--mute_clips` What this does: Mute clip audio (Default is False)
 - `--recurse` What this does: Scan input directory recursively  (Default is False)

 - `--shuffle` What this does: Shuffles the clips instead of sorting them alphabetically (Default is False)

 - `--allow_repeat` What this does: Allow uses of clips that have been used in previous montages (Default is False)

 - `--no_database_save` What this does: Do not save montages in the database (Default is False)

 - `--no_banners` What this does: Disabled banner text (Default is False)

 - `-montage` What this does: Recreate montage by id, Overrides count, shuffle and allow_repeat arguments (Default is False)

 - `-ignore_database` What this does: doesnt use any clips stored in the data base (Default is False)

 - `-vcodec` What this does: The video codec that is used to encode the output (Default is "libx264") (see below)

 -  `-acodec` What this does: The audio codec that is used to encode the output (Default is "aac") (see below) 

**Refer to ffempeg documentation to see available codec **

## Contributors:
 - Gabriele M. Nunez
 - Austin Harms
 - Alexander Hackbart

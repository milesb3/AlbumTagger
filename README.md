### Project description
This is a python3 project meant to make tagging the metadata of albums of mp3 files easier. Upon creating a valid 'album tagger definition' (.atd) file (see example.atd and empty-template.atd in this project) and placing it in the directory containing the audio files making up the album you wish to tag, the user can then run
```
python3 tag_album.py <path/to/filename.atd>
```
to automatically convert files to mp3 (if necessary) and tag them based on the input .atd file. This is done using a custom class defined in AlbumInfo.py that parses .atd files for mp3 metadata.

### Dependencies
This program is functional on my Ubuntu 24.04.2 LTS system, and relies on these dependencies:
- ffmpeg (for converting audio files that do not have extension mp3 to mp3).
- The eyeD3 python library (for tagging the mp3 files).
- musicbrainzngs python3 library (used for pulling metadata in get_musicbrainz_metadata.py)

### Future plans for this project
- Add more options to tag_album.py, such as printing the parsed metadata from the .atd file and not printing the ffmpeg output.
- Add option to set album cover on a track by track basis.
- Try rewriting the project in Rust.

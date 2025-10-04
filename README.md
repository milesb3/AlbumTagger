### Project description
This is a python3 project meant to make tagging the metadata of albums of mp3 files easier. Upon creating a valid 'album tagger definition' (.atd) file (see example.atd and empty-template.atd in this project) and placing it in the directory containing the audio files making up the album you wish to tag, the user can then run
```
python3 tag_album.py <path/to/filename.atd>
```
to automatically convert files to mp3 (if necessary) and tag them based on the input .atd file. This is done using a custom class defined in AlbumInfo.py that parses .atd files for mp3 metadata.

### Dependencies
I have successfully used this project on Ubuntu 24.04.4 LTS and Fedora 42, so any modern Linux distrobution should work. You will need these dependencies installed:
- ffmpeg (for converting audio files that do not have extension mp3 to mp3).
- The eyeD3 python library (for tagging the mp3 files).
- musicbrainzngs python3 library (used for pulling metadata in get_musicbrainz_metadata.py)

### Future plans for this project
- Rewrite in C++ (see cpp_version directory).
- Create a function to more quickly or automatically rename files for simpler .atd file usage.
- Add option to set album cover on a track by track basis.

import os

NUM_TRACKINFO_ATTRIBUTES :int = 5

class AlbumInfo:
    def __init__(self, atd_file :str):
        '''
        Takes in a file with a '.atd' (album tagger definition) file extension and constructs an AlbumInfo object
        to be used in tag_album.py for converting audio files to mp3 and tagging them.
        '''
        #Define default parameter valuess to be set later in this constructor based on atd_file
        self.dir = ""
        self.album :str = ""
        self.album_artist :str = ""
        self.cover_path :str = ""
        self.cover_bytes :bytes = 0
        self.year :int = 0
        self.genre :str = ""
        self.tracks_info :list[TrackInfo] = []

        #Determine album path directory from input atd file
        self.dir = os.path.dirname(atd_file)

        #Read album wide parameters from atd file
        atd_info = open(atd_file, "r")
        while (atd_line := atd_info.readline()):
            #ignore any commented lines
            if (atd_line[0] == "#"):
                continue
            #Exit this loop once entered track info section
            elif ("filename" in atd_line):
                break
            #Check for lines containing album wide parameters (telltale '=')
            atd_line = atd_line.split("=")
            if (len(atd_line) > 1):
                param_name = atd_line[0].strip(" ")
                param_val = atd_line[1].strip(" \n")
                if (param_name == "album"):
                    self.album = param_val
                elif (param_name == "album_artist"):
                    self.album_artist = param_val
                elif (param_name == "cover_file_path"):
                    self.cover_path = param_val
                elif (param_name == "year"):
                    try:
                        self.year = int(param_val)
                    except:
                        print(f'Warning! Unable to read year tag from {atd_file}. Year must be written as an integer.')
                elif (param_name == "genre"):
                    self.genre = param_val
        #Extract track info and store in AlbumInfo object's TrackInfo list
        while (atd_line := atd_info.readline()):
            self.tracks_info.append(TrackInfo(atd_line.split("|")))
        atd_info.close()
        #Convert cover into bytes
        try:
            self.cover_bytes = open(f'{self.dir}{self.cover_path}', "rb").read()
        except Exception as error:
            print(f'Warning! Failed to convert {self.dir}{self.cover_path} to bytes. Received error:')
            print(error)

    def print_attributes(self):
        '''
        Prints object attributes (useful for testing).
        '''
        print(f'dir = {self.dir}')
        print(f'album = {self.album}')
        print(f'album_artist = {self.album_artist}')
        print(f'cover_path = {self.cover_path}')
        print(f'year = {self.year}')
        print(f'genre = {self.genre}')
        for track in self.tracks_info:
            track.print_attributes()

class TrackInfo:
    def __init__(self, atd_track_entry :list[str]):
        '''
        Called by AlbumInfo class to organize individual track info read from .atd files
        '''
        #Define default parameter values to be set by input string list
        self.filename :str = ""
        self.disc_num :int = 0
        self.track_num :int = 0
        self.track_title :str = ""
        self.artist :str = ""

        #Check if input string list is the correct length
        if (len(atd_track_entry) != NUM_TRACKINFO_ATTRIBUTES):
            print("Warning! Could not add track info for a track due to incorrect input atd_track_entry string list length")
            return

        #Assign input list of strings to TrackInfo attributes
        self.filename = atd_track_entry[0].strip(" \t\n")
        try:
            self.disc_num = int(atd_track_entry[1].strip(" \t\n"))
        except:
            print(f'Warning! Unable to read disc_num tag for track tied to file {self.filename}. disc_num must be written as an integer.')
        try:
            self.track_num = int(atd_track_entry[2].strip(" \t\n"))
        except:
            print(f'Warning! Unable to read tack_num tag for track tied to file {self.filename}. track_num must be written as an integer.')
        self.track_title = atd_track_entry[3].strip(" \t\n")
        self.artist = atd_track_entry[4].strip(" \t\n")

    def print_attributes(self):
        '''
        Prints all attributes of a TrackInfo object (useful for testing)
        '''
        print(f'disc {self.disc_num} track {self.track_num}: "{self.track_title}" by {self.artist} stored in {self.filename}')
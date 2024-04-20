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
        #TODO add attribute to store cover bytes
        self.year :int = 0
        self.genre :str = ""
        self.tracks_info :list[TrackInfo] = []

        #TODO (constructor part lol)

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

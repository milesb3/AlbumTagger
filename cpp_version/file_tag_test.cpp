#include "file_tag_test.hpp"

//TODO add track metadata class to store metadata
void tagTrack(TagLib::FileRef track_ref) {


	TagLib::FileRef f("Latex Solar Beef.mp3");

	f.tag()->setAlbum("Fillmore East");
	f.save();

	TagLib::FileRef g("Free City Rhymes.ogg");
	TagLib::String album = g.tag()->album(); // album == "NYC Ghosts & Flowers"

	g.tag()->setTrack(1);
	g.save();
}

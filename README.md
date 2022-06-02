## Find Tunes: Discogs(tm) collection searcher

Discogs provides track names and credits for most music releases, but you cannot search their db by a track name or a credit.

This project will store that data for your collection in a local Postgresql db, which can then be queried by track or musician.

The Minimum Viable Product will only store your collection's releases and songs in its db. Searching for a song name
will retrun all releases with that name in the track list.

Written in CPython 3.10.

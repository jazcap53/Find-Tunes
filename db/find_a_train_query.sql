select r.discogs_release_string
from tu_release r
join tu_song_release sr
on r.release_id = sr.release_id
join tu_song s
on s.song_id = sr.song_id
where s.song_title = 'take the "a" train';

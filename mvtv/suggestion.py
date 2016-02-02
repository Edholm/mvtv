from pathlib import PurePath, Path
from guessit import guessit
from titlecase import titlecase
from rtorrent import RTorrent


class PathSuggester(object):
    def __init__(self, base_path='/mnt/storage', tv_path='TV-Shows'):
        if '~' in base_path:
            raise ValueError('~ (tilde) is not supported')

        base_path = Path(base_path)
        self._tv_path = base_path / tv_path

    def _valid_guess(self, guess):
        return guess and guess['type'] == 'episode' and 'series' in guess

    def suggest(self, src, append_season=True):
        ''' Takes a source path and suggest a destination path'''
        src = PurePath(src)
        dest = None
        guess = guessit(src.name)

        # Try to find the torrent in rtorrent and use that name instead.
        if not self._valid_guess(guess):
            rt = RTorrent()
            print("via rtorrent")
            torrent = rt.search_by_path(str(src))
            guess = guessit(torrent[0]) if torrent else None  # 0 == name

        if self._valid_guess(guess):
            dest = self._tv_path / titlecase(guess['title'])
            if append_season and 'season' in guess:
                dest = dest / ('S{0:02d}'.format(guess['season']))

            # Is it a single episode or a bundle?
            if 'episode' in guess:
                dest = dest / src.name

        return dest

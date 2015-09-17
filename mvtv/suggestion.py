from pathlib import PurePath, Path
from guessit import guess_file_info
from titlecase import titlecase


class PathSuggester(object):
    def __init__(self, base_path='/mnt/storage', tv_path='TV-Shows'):
        if '~' in base_path:
            raise ValueError('~ (tilde) is not supported')

        base_path = Path(base_path)
        self._tv_path = base_path / tv_path

    def suggest(self, src, append_season=True):
        ''' Takes a source path and suggest a destination path'''
        src = PurePath(src)
        dest = None

        guess = guess_file_info(src.name)
        if guess['type'] == 'episode':
            dest = self._tv_path / titlecase(guess['series'])
            if append_season and 'season' in guess:
                dest = dest / ('S' + str(guess['season']))

            # Is it a single episode or a bundle?
            if 'episodeNumber' in guess:
                dest = dest / src.name

        return dest

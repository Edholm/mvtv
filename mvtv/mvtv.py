#!/usr/bin/python3

from suggestion import PathSuggester
from rtorrent import RTorrent
from pathlib import Path
from colorama import Fore


def main():
    args, sources = cmd_args()

    ps = PathSuggester()
    for src in sources:
        src = Path(src)
        dest = ps.suggest(src)
        src_s = str(src.resolve())
        dest_s = str(dest)

        rt = RTorrent()
        torrent = rt.search_by_path(src_s)

        t_mark = Fore.BLUE + '[T] ' + Fore.RESET if not torrent else ''
        print(t_mark + Fore.YELLOW + src_s + Fore.MAGENTA + " -> " +
              Fore.GREEN + dest_s + Fore.RESET)

        # Do the actual moving
        if not dest.is_dir():
            dest.mkdir(parents=True)
        src.rename(dest)


def cmd_args():
    from optparse import OptionParser
    parser = OptionParser(description="Move TV-shows to suggested destination")
    return parser.parse_args()

if __name__ == '__main__':
    main()

#!/usr/bin/python3

from suggestion import PathSuggester
from rtorrent import RTorrent
from pathlib import Path
from colorama import Fore


def main():
    args = cmd_args()

    ps = PathSuggester()
    for src in args.sources:
        src = Path(src)
        dest = ps.suggest(src)
        src_s = str(src.resolve())
        dest_s = str(dest)

        rt = RTorrent()
        torrent = rt.search_by_path(src_s)

        t_mark = Fore.BLUE + '[T] ' + Fore.RESET if torrent else ''
        print(t_mark + Fore.YELLOW + src_s + Fore.MAGENTA + " -> " +
              Fore.GREEN + dest_s + Fore.RESET)

        # Do the actual moving
        if not args.dry_run and not dest.is_dir():
            dest.mkdir(parents=True)
        # Note: this does not support moving between hard drives.
        if not args.dry_run:
            rt.close(torrent)
            rt.set_base_path(dest_s)
            src.rename(dest)
            rt.start(torrent)


def cmd_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Move TV-shows to suggested destination")
    # parser.add_argument('-d', '--disable-rtorrent', action='store_false', dest='use_rtorrent',
    #                    help='Disable rtorrent interface.')
    parser.add_argument('-t', '--dry-run', action='store_true', dest='dry_run',
                        help='Do not actually move the folders...')
    parser.add_argument('sources', metavar='SOURCE', type=str, nargs='+',
                                           help='Sources to move to a suggested destination')

    return parser.parse_args()

if __name__ == '__main__':
    main()

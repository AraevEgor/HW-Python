from argparse import ArgumentParser
from copy import copy
from datetime import datetime
from pathlib import Path
import stat


DESC = "Custom script for listing given files and the contents of given directories"


def ls(args):
    """Defined as a function for recursive calls"""
    files = []
    dirs = {}
    for file in args.files:
        p = Path(file)
        # if -d flag is present, treat directories as files
        if p.is_dir() and not args.directory:
            # list files in a directory, skip those starting with . if no -a flag
            l = [f for f in p.glob("*") if (not f.name.startswith(".")) or args.all]
            dirs[str(p)] = l
            # if -R flag is present, recursively call the function on subdirectories
            if args.R:
                tmp = copy(args)
                tmp.files = [f for f in l if f.is_dir()]
                _, rdirs = ls(tmp)
                dirs.update(rdirs)
        # add files to list
        else:
            files.append(p)
    return files, dirs


def ls_sort(l, args):
    """Sort accordign to specified flags. Assumes one or no flags have been passed, 
    no protection from mutually exclusive flags (bad, but too lazy to add it)"""
    tmp = copy(l)
    keyfunc = lambda x: x.name
    if args.ext:
        keyfunc = lambda x: x.suffix
    if args.time or args.utime or args.size:
        tmp = [(i, i.stat()) for i in l]
        if args.time:
            keyfunc = lambda x: x[1].st_mtime
        if args.utime:
            keyfunc = lambda x: x[1].st_atime
        if args.size:
            keyfunc = lambda x: x[1].st_size
    res = sorted(tmp, key=keyfunc, reverse=args.r)
    if args.time or args.utime or args.size:
        res = [i[0] for i in res]
    return res


def ls_l(file, args):
    """Format given file into long output format"""
    s = file.stat()
    size = s.st_size
    # add human-readable file-sizes if -h flag is present
    if args.h:
        sizes = ("K", "M", "G", "T", "P", "E", "Z", "Y")
        count = -1
        while size // 1024 > 0:
            size = size // 1024
            count += 1
        if count > -1:
            size = f"{size} {sizes[count]}iB"
    time = s.st_mtime
    # use last access time if -u flag is present
    if args.utime:
        time = s.st_atime
    time = datetime.fromtimestamp(time).isoformat(sep=" ", timespec="seconds")
    return f"{stat.filemode(s.st_mode)}  {s.st_nlink}  {s.st_uid}  {s.st_gid}  {time}  {str(size).rjust(10)}  {file.name}"


def ls_formatted_print(files, dirs, args):
    """Print all specified files, then contents of specified directories in specified format"""
    # sort files if needed
    if not args.f:
        files = ls_sort(files, args)
    for file in files:
        # print files, in long format if -l flag is present
        if args.long:
            print(ls_l(file, args))
        else:
            print(file)
    # the same for every dir specified
    for d in dirs:
        if len(files) > 0:
            print()
        print(f"Directory {d}:")
        if not args.f:
            dirs[d] = ls_sort(dirs[d], args)
        for file in dirs[d]:
            if args.long:
                print(f"    {ls_l(file, args)}")
            else:
                print(f"    {file.name}")


if __name__ == "__main__":
    parser = ArgumentParser(description=DESC, add_help=False)
    parser.add_argument("files", nargs="*", default=".")
    parser.add_argument("--help", action="help", help="Help message")
    parser.add_argument(
        "-h",
        "--human-readable",
        action="store_true",
        help="Format filesizes to readable format",
        dest="h",
    )
    parser.add_argument(
        "-l",
        "--format=long",
        "--format=verbose",
        action="store_true",
        dest="long",
        help="Long format",
    )
    parser.add_argument("-a", "--all", action="store_true", help="Show hidden files")
    parser.add_argument("-R", action="store_true", help="Recurisve")
    parser.add_argument("-r", action="store_true", help="Reverse order")
    parser.add_argument("-f", action="store_true", help="Do not sort")
    parser.add_argument(
        "-d", "--directory", action="store_true", help="Treat dirs as files"
    )
    parser.add_argument(
        "-t",
        "--sort=time",
        action="store_true",
        help="Sort by last modification time",
        dest="time",
    )
    parser.add_argument(
        "-S", "--sort=size", action="store_true", help="Sort by filesize", dest="size"
    )
    parser.add_argument(
        "-X",
        "--sort=extension",
        action="store_true",
        help="Sort by file extension",
        dest="ext",
    )
    parser.add_argument(
        "-u",
        "--time=atime",
        "--time=access",
        "--time=use",
        action="store_true",
        help="Sort by last access time",
        dest="utime",
    )
    args = parser.parse_args()

    ls_formatted_print(*ls(args), args)

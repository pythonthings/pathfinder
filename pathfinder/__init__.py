"""pathfinder package."""
#
# Copyright 2009 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

import os

from pathfinder import filters


def walk_and_filter(filepath, pathfilter, ignore=None, abspath=None, depth=None):
    """Walk the file tree and filter it's contents."""
    return list(walk_and_filter_generator(filepath, pathfilter, ignore, abspath, depth))


def walk_and_filter_generator(  # noqa:C901
    filepath, pathfilter, ignore=None, abspath=None, depth=None
):
    """
    Walk the file tree and filter it's contents.

    To ignore any paths an specify an ignore filter.

    To return absolute paths pass True for the abspath parameter.

    To limit how deep into the tree you travel, specify the depth parameter.
    """
    # by default no depth limit is enforced
    if depth is None:
        depth = -1
    else:
        depth = int(depth)

    if abspath is None:
        abspath = False

    if os.path.isdir(filepath):
        base_path = os.path.normpath(filepath)
    else:
        base_path = os.path.normpath(os.path.dirname(filepath))

    for root, dirs, files in os.walk(base_path):

        # descend the tree to a certain depth
        level = len(root.split(base_path)[1].split(os.sep))
        if level > depth and depth != -1:
            break

        # process in order
        dirs.reverse()
        ignored = []
        for adir in dirs:
            dirpath = os.path.normpath(os.path.join(root, adir))
            if ignore and ignore.accepts(dirpath):
                ignored.append(adir)
                continue
            if pathfilter.accepts(dirpath):
                if abspath:
                    hit_path = os.path.abspath(dirpath)
                else:
                    hit_path = os.path.join(base_path, dirpath)
                yield hit_path

        # remove the dirs we are ignoring
        for adir in ignored:
            dirs.remove(adir)

        for afile in files:
            filepath = os.path.normpath(os.path.join(root, afile))
            if ignore and ignore.accepts(filepath):
                continue
            if pathfilter.accepts(filepath):
                if abspath:
                    filepath = os.path.abspath(filepath)
                yield filepath


def pathfind(
    filepath,
    just_dirs=None,
    just_files=None,
    regex=None,
    fnmatch=None,
    filter=None,  # skipcq: PYL-W0622
    ignore=None,
    abspath=None,
    depth=None,
):
    """Warn of deprecated function."""
    import warnings

    warnings.warn("Deprecated. Please use find.", DeprecationWarning)
    return find(
        filepath, just_dirs, just_files, regex, fnmatch, filter, ignore, abspath, depth
    )


def find(
    directory_path,
    just_dirs=None,
    just_files=None,
    regex=None,
    fnmatch=None,
    filter=None,  # skipcq: PYL-W0622
    ignore=None,
    abspath=None,
    depth=None,
):
    """Find paths in the tree rooted at filepath."""
    import warnings

    warnings.warn("Deprecated. Please use find_paths.", DeprecationWarning)
    return list(
        find_paths(
            directory_path,
            just_dirs,
            just_files,
            regex,
            fnmatch,
            filter,
            ignore,
            abspath,
            depth,
        )
    )


def find_paths(
    directory_path,
    just_dirs=None,
    just_files=None,
    regex=None,
    fnmatch=None,
    filter=None,  # skipcq: PYL-W0622
    ignore=None,
    abspath=None,
    depth=None,
):
    """Find paths in the tree rooted at filepath."""
    if just_dirs:
        path_filter = filters.DirectoryFilter()
    elif just_files:
        path_filter = filters.FileFilter()
    elif regex:
        path_filter = filters.RegexFilter(regex)
    elif fnmatch:
        path_filter = filters.FnmatchFilter(fnmatch)
    elif not filter:
        path_filter = filters.AlwaysAcceptFilter()
    else:
        path_filter = filter

    return walk_and_filter_generator(
        directory_path, path_filter, ignore, abspath, depth
    )

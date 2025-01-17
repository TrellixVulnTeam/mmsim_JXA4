import os
import tarfile
from pathlib import Path
from urllib.request import urlretrieve

from .typing import TarMembers


def clean_tar_members(members: TarMembers) -> TarMembers:
    """
    Strip .tar components (i.e.: remove top-level directory) from members.

    Parameters
    ----------
    members
        A list of .tar members.

    Returns
    -------
        A clean .tar member list with the stripped components.
    """
    clean = []
    for member in members:
        path = Path(member.name)
        member.name = str(path.relative_to(path.parts[0]))
        clean.append(member)
    return clean


def select_tar_members(
    members: TarMembers, parent: Path, new_path: Path
) -> TarMembers:
    """
    Select .tar members given a parent path and rename them to have a new
    path instead.

    Parameters
    ----------
    members
        A list of .tar members.
    parent
        Parent path to filter members.
    new_path
        New member path.

    Returns
    -------
    A clean .tar member list with the selected, renamed components.
    """
    clean = []
    for member in members:
        path = Path(member.name)
        if path.is_absolute():
            raise NotImplementedError('Please, report this unexpected error!')
        path = path.relative_to(path.parts[0])
        if path.parent != parent:
            continue
        member.name = str(new_path / path.name)
        clean.append(member)
    return clean


def download_micromouseonline_mazes(download_path: Path):
    """
    Download Micromouseonline mazes.

    Parameters
    ----------
    download_path
        Where to download the maze files to.
    """
    url = (
        'https://github.com/micromouseonline/mazefiles/'
        'archive/master.tar.gz'
    )
    reveal_tar, headers = urlretrieve(url)
    with tarfile.open(reveal_tar) as tar:
        members = clean_tar_members(tar.getmembers())
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, str(download_path), members)
    os.remove(reveal_tar)

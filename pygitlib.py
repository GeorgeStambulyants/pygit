import argparse
import collections
import configparser
from genericpath import isdir
import hashlib
import os
import re
import sys
import zlib
import typing


argparser = argparse.ArgumentParser(description="The stupid content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository")
argsp.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository")

class GitRepository:
    """A git repository"""
    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path: str, force: bool=False) -> None:
        self.worktree = path
        self.gitdir = os.path.join(path, ".pygit")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion {vers}")


def cmd_init(args: argparse.Namespace) -> None:
    repo_create(args.path)


def repo_path(repo: GitRepository, *path: str) -> str:
    """Compute path under repo's gitdir."""
    if not repo.gitdir:
        raise Exception("repo.gitdir is empty")
    return os.path.join(repo.gitdir, *path)


def repo_file(repo: GitRepository, *path: str, mkdir: bool=False) -> typing.Union[None, str]:
    """
    Same as repo_path, but create dirname(*path) if absent. For
    example, repo_file(r, "refs", "remotes", "origin", "HEAD") will create
    .git/refs/remotes/origin.
    """
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)


def repo_dir(repo: GitRepository, *paths: str, mkdir=False) -> typing.Union[None, str]:
    """Same as repo_path, but mkdir *path is absend if mkdir."""
    path = repo_path(repo, *paths)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"Not a directory {path}")

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def repo_create(path: str) -> GitRepository:
    """Create a new repository at path."""
    repo = GitRepository(path, True)

    if not repo.worktree:
        raise Exception("repo.worktree is empty")

    # First, we make sure the path doesn't exist of it an empty dir
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory!")
        if os.listdir(repo.worktree):
            raise Exception(f"{path} is not empty")
    else:
        os.makedirs(repo.worktree)

    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # .git/description
    filename = repo_file(repo, "description")
    if not filename:
        raise Exception("Something went wrong")
    with open(filename, "w") as f:
        f.write("Unnamed repository: edit this file 'description' to name the repository.\n")

    # .git/HEAD
    filename = repo_file(repo, "HEAD")
    if not filename:
        raise Exception("Something went wrong")
    with open(filename, "w") as f:
        f.write("ref: refs/heads/master\n")

    filename = repo_file(repo, "config")
    if not filename:
        raise Exception("Something went wrong")
    with open(filename, "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo


def repo_default_config() -> configparser.ConfigParser:
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    print(type(args))

    if   args.command == "add"         : pass # cmd_add(args)
    elif args.command == "cat-file"    : pass # cmd_cat_file(args)
    elif args.command == "checkout"    : pass # cmd_checkout(args)
    elif args.command == "commit"      : pass # cmd_commit(args)
    elif args.command == "hash-object" : pass # cmd_hash_object(args)
    elif args.command == "init"        : cmd_init(args)
    elif args.command == "log"         : pass # cmd_log(args)
    elif args.command == "ls-tree"     : pass # cmd_ls_tree(args)
    elif args.command == "merge"       : pass # cmd_merge(args)
    elif args.command == "rebase"      : pass # cmd_rebase(args)
    elif args.command == "rev-parse"   : pass # cmd_rev_parse(args)
    elif args.command == "rm"          : pass # cmd_rm(args)
    elif args.command == "show-ref"    : pass # cmd_show_ref(args)
    elif args.command == "tag"         : pass # cmd_tag(args)


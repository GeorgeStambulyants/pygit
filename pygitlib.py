import argparse
import collections
import configparser
import hashlib
import os
import re
import sys
import zlib


argparser = argparse.ArgumentParser(description="The stupid content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    
    if   args.command == "add"         : pass # cmd_add(args)
    elif args.command == "cat-file"    : pass # cmd_cat_file(args)
    elif args.command == "checkout"    : pass # cmd_checkout(args)
    elif args.command == "commit"      : pass # cmd_commit(args)
    elif args.command == "hash-object" : pass # cmd_hash_object(args)
    elif args.command == "init"        : pass # cmd_init(args)
    elif args.command == "log"         : pass # cmd_log(args)
    elif args.command == "ls-tree"     : pass # cmd_ls_tree(args)
    elif args.command == "merge"       : pass # cmd_merge(args)
    elif args.command == "rebase"      : pass # cmd_rebase(args)
    elif args.command == "rev-parse"   : pass # cmd_rev_parse(args)
    elif args.command == "rm"          : pass # cmd_rm(args)
    elif args.command == "show-ref"    : pass # cmd_show_ref(args)
    elif args.command == "tag"         : pass # cmd_tag(args)


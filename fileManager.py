import os
import shutil
import argparse
from datetime import datetime

"""
Command          | Description
-----------------|-----------------------------------------------
list             | Lists all files and folders in a directory
                 | Usage: list [path]
                 | Example: python file_manager.py list Documents/

create-file      | Creates a new empty file
                 | Usage: create-file <path>
                 | Example: python file_manager.py create-file notes.txt

create-folder    | Creates a new folder (directory)
                 | Usage: create-folder <path>
                 | Example: python file_manager.py create-folder test_dir

delete           | Deletes a file or folder (recursively for folders)
                 | Usage: delete <path>
                 | Example: python file_manager.py delete old_file.txt

move             | Moves or renames a file/folder to a new location
                 | Usage: move <src> <dest>
                 | Example: python file_manager.py move a.txt backup/

copy             | Copies a file or folder (recursively for folders)
                 | Usage: copy <src> <dest>
                 | Example: python file_manager.py copy data/ backup/

rename           | Renames a file or folder
                 | Usage: rename <src> <dest>
                 | Example: python file_manager.py rename old.txt new.txt

info             | Shows details (size, type, last modified time)
                 | Usage: info <path>
                 | Example: python file_manager.py info notes.txt

read             | Displays the content of a text file in terminal
                 | Usage: read <path>
                 | Example: python file_manager.py read notes.txt

search           | Searches for files/folders by name (case-insensitive)
                 | Usage: search <keyword> [path]
                 | Example: python file_manager.py search report ./Documents
"""

def list_dir(path):
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                print(f"[DIR]  {entry}")
            else:
                print(f"       {entry}")
    except FileNotFoundError:
        print("Directory not found.")

def create_file(path):
    with open(path, "w") as f:
        pass
    print(f"File created: {path}")

def create_folder(path):
    os.makedirs(path, exist_ok=True)
    print(f"Folder created: {path}")

def delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Folder deleted: {path}")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"File deleted: {path}")
    else:
        print("Path not found.")

def move(src, dest):
    shutil.move(src, dest)
    print(f"Moved: {src} → {dest}")

def copy(src, dest):
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    print(f"Copied: {src} → {dest}")

def rename(src, dest):
    os.rename(src, dest)
    print(f"Renamed: {src} → {dest}")

def info(path):
    if not os.path.exists(path):
        print("Path not found.")
        return
    stats = os.stat(path)
    print(f"Name: {os.path.basename(path)}")
    print(f"Type: {'Directory' if os.path.isdir(path) else 'File'}")
    print(f"Size: {stats.st_size} bytes")
    print(f"Modified: {datetime.fromtimestamp(stats.st_mtime)}")

def read_file(path):
    if not os.path.isfile(path):
        print("File not found.")
        return
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())

def search(keyword, path="."):
    found = False
    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            if name.lower().startswith(keyword.lower()):
                print(os.path.join(root, name))
                found = True
    if not found:
        print("No matching files or folders found.")

def main():
    parser = argparse.ArgumentParser(description="Python CLI File Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    list_parser = subparsers.add_parser("list", help="List files in directory")
    list_parser.add_argument("path", nargs="?", default=".", help="Path to list")

    # create-file
    cf_parser = subparsers.add_parser("create-file", help="Create a new file")
    cf_parser.add_argument("path", help="Path of new file")

    # create-folder
    cdir_parser = subparsers.add_parser("create-folder", help="Create a new folder")
    cdir_parser.add_argument("path", help="Path of new folder")

    # delete
    del_parser = subparsers.add_parser("delete", help="Delete a file or folder")
    del_parser.add_argument("path", help="Path to delete")

    # move
    mv_parser = subparsers.add_parser("move", help="Move file/folder")
    mv_parser.add_argument("src", help="Source path")
    mv_parser.add_argument("dest", help="Destination path")

    # copy
    cp_parser = subparsers.add_parser("copy", help="Copy file/folder")
    cp_parser.add_argument("src", help="Source path")
    cp_parser.add_argument("dest", help="Destination path")

    # rename
    rn_parser = subparsers.add_parser("rename", help="Rename a file/folder")
    rn_parser.add_argument("src", help="Old name")
    rn_parser.add_argument("dest", help="New name")

    # info
    info_parser = subparsers.add_parser("info", help="Show file/folder info")
    info_parser.add_argument("path", help="Path to check")

    # read
    read_parser = subparsers.add_parser("read", help="Read and print file content")
    read_parser.add_argument("path", help="File to read")

    # search
    search_parser = subparsers.add_parser("search", help="Search files/folders")
    search_parser.add_argument("keyword", help="Keyword to search for")
    search_parser.add_argument("path", nargs="?", default=".", help="Directory to search in")

    args = parser.parse_args()

    if args.command == "list":
        list_dir(args.path)
    elif args.command == "create-file":
        create_file(args.path)
    elif args.command == "create-folder":
        create_folder(args.path)
    elif args.command == "delete":
        delete(args.path)
    elif args.command == "move":
        move(args.src, args.dest)
    elif args.command == "copy":
        copy(args.src, args.dest)
    elif args.command == "rename":
        rename(args.src, args.dest)
    elif args.command == "info":
        info(args.path)
    elif args.command == "read":
        read_file(args.path)
    elif args.command == "search":
        search(args.keyword, args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

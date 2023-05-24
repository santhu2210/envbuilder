# .env file builder
import os
import re
import sys
from os import walk
from os.path import splitext, join

# default environments directory names
Environ_dir = [
    'env','venv','.env','.venv','ENV','VENV','env.bak','venv.bak','.git'
    ]
py_get_env_syntax = ['os.environ','os.getenv','os.environ.get']

def read_file_return_envs(file):
    """
    read a file and return the declared envs list
    Args:
        file - which file to read (str)
    Return:
        env_list - list of envs (list)
    """
    env_list = []
    with open(file) as file:
        for line in file:
            if any(True if en in line else False for en in py_get_env_syntax):
                env_vars = re.findall(r"(['\"])(.*?)\1", line)
                env_list.append(env_vars[0][1])
    return env_list

def select_files(root, files):
    """
    simple logic here to filter out .py files
    Args:
        root - root directory path (str)
        files - files path (str)
    Return:
        selected_files = python files list (list)
    """
    selected_files = []
    for file in files:
        full_path = join(root, file)
        ext = splitext(file)[1]
        if ext == ".py":
            selected_files.append(full_path)
    return selected_files

def build_env(path, skip_dir=None):
    """
    Scan provided project path and build/append env file there
    Args:
        path - where to begin folder scan and store .env file (str)
        skip_dir - to skip the directory on scan (str)
    """
    selected_files = []
    env_list = []
    if skip_dir:
        Environ_dir.append(skip_dir)
    for root, dirs, files in walk(path):
        if all(True if env not in root else False for env in Environ_dir):
            selected_files += select_files(root, files)
    for file in selected_files:
        env_list += read_file_return_envs(file)
    all_env_var_set= set(env_list)
    if os.path.isfile(os.path.join(path,'.env')):
        with open(os.path.join(path,'.env'),'r+') as fb:
            exst_env_var_set = set([var.rsplit('=')[0] for var in fb.read().splitlines()])
            missed_envs = all_env_var_set - exst_env_var_set
            for env in missed_envs:
                fb.write(f"\n{env}=")
    else:
        with open(os.path.join(path,'.env'),'w') as fb:
            for env in all_env_var_set:
                fb.write(f"{env}=\n")

if __name__ == '__main__':
    if len(sys.argv)>=2:
        if len(sys.argv)==3:
            # including skip folder name from user input
            build_env(sys.argv[1], sys.argv[2])
        else:
            # include all directory in project folder
            build_env(sys.argv[1])
    else:
        print("Please provide the valid full project path to scan, next to script name")
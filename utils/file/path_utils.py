import glob
import os
import shutil


def is_path_exist(path):
    # Check whether the path exists
    return os.path.exists(path)


def check_path(path, mkdir=True, log=True):
    # Ensure the directory containing `path` exists; create it when missing
    dir = path if os.path.isdir(path) else os.path.abspath(os.path.dirname(path))  # use path itself if a directory, else its parent
    is_exist = is_path_exist(dir)
    if mkdir and not is_path_exist(dir):
        try:
            os.makedirs(dir, exist_ok=True)
            if log:
                print(f'The path does not exist, makedir: {dir}: Success')
        except Exception:
            raise RuntimeError(f'The path does not exist, makedir {dir}: Failed')
    return is_exist


def makedir(path):
    os.makedirs(path, exist_ok=True)  # Recursively create the directory; no error if it already exists


def walk_path(base):
    # Walk the `base` directory and return every (root, dirs, files) tuple
    return [[root, dirs, files] for root, dirs, files in os.walk(base)]


def list_dir(base, absolute=False):
    # List immediate sub-directories of `base`
    if absolute:  # return absolute paths
        return [os.path.join(base, d) for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
    else:
        return [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]


def list_file(base, absolute=False):
    # List immediate files inside `base`
    if absolute:  # return absolute paths
        return [os.path.join(base, f) for f in os.listdir(base) if os.path.isfile(os.path.join(base, f))]
    else:
        return [f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f))]


def filter_dir(path, pattern, absolute=False, recursive=False):
    # Recursively glob directories under `path` matching `pattern`
    dirs = glob.glob(pattern, root_dir=path, recursive=recursive)
    dirs = [dir for dir in dirs if os.path.isdir(os.path.join(path, dir))]
    dirs = [os.path.join(path, dir) for dir in dirs] if absolute else dirs
    return dirs


def filter_file(path, pattern, absolute=False, recursive=False):
    # Recursively glob files under `path` matching `pattern`
    files = glob.glob(pattern, root_dir=path, recursive=recursive)
    files = [os.path.abspath(os.path.join(path, file)) for file in files] if absolute else files
    return files


def remove_dir(dirs, force=True):
    # Remove the given directory or directories
    if isinstance(dirs, str):
        dirs = [dirs]
    for dir in dirs:
        if os.path.isdir(dir):
            if force:
                os.system(f'rm -rf {dir}')
            else:
                os.rmdir(dir)
        else:
            print(f'Error: {dir} is not a directory')


def remove_file(files):
    # Remove the given file or files
    if isinstance(files, str):
        files = [files]
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
        else:
            print(f'Warning: {file} is not a file')


def rename_file(file, new_name):
    # Batch rename files
    if isinstance(file, str):
        file = [file]
    if isinstance(new_name, str):
        new_name = [new_name]
    assert len(file) == len(new_name)
    for f, n in zip(file, new_name):
        if os.path.isfile(f):
            os.rename(f, n)
        else:
            print(f'Error: {f} is not a file')


def copy_file(src_path, target_path):
    # Copy a file to the target path
    if is_path_exist(src_path):
        check_path(target_path)
        shutil.copy(src_path, target_path)
        print(f'Copy {src_path} to {target_path}: Success')
    else:
        print(f'Error: {src_path} is not a file')


def get_basename(path, suffix=False):
    # Get the file basename (with or without extension)
    return os.path.basename(path) if suffix else os.path.splitext(os.path.basename(path))[0]

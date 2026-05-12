import zipfile

from .path_utils import *
from .read_utils import *
from .write_utils import *


def zip_files(output, files):
    # Pack the given files into a single zip archive (files only, not directories)
    assert '.zip' in output, 'output file must be a zip file'
    with zipfile.ZipFile(output, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))

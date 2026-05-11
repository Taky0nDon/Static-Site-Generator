import os
import shutil
from pathlib import Path

def copy_to_public(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    os.mkdir(dst)

    for file in os.listdir(src):
        original_file = src.joinpath(file)
        new_file = dst.joinpath(file)
        if original_file.is_dir():
            copy_to_public(original_file, new_file)
        else:
            shutil.copy(original_file, new_file)

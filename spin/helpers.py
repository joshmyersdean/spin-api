import zipfile
import os
import shutil


def unzip_file(zip_path: str, extract_to: str) -> None:
    """
    Unzips a file to a specified directory. All files in the zipped folder
    will be placed directly in the target directory without preserving folder structure.

    :param zip_path: The path to the zip file.
    :param extract_to: The directory where the files should be extracted.
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if not filename:
                # If there is a directory in the zip, skip it
                continue
            source = zip_ref.open(member)
            target = open(os.path.join(extract_to, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
    print(f"File unzipped successfully to {extract_to}")

import glob
import os
import shutil
import zipfile
from distutils.dir_util import copy_tree

# Absolute path to download folder with the slash at the end
DOWNLOAD_FOLDER = '...'  # e.g. '/home/anton/Загрузки/'
REMOVE_ZIP_FROM_DOWNLOADS = False

# You can change it if you want
STYLE_TAG = """
    <link rel="stylesheet" 
       href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" 
       integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" 
       crossorigin="anonymous">
"""
LOAD_STATIC_TAG = '{% load static %}'
YATUBE_FOLDER = 'yatube'


def main():
    project_dir: str = os.path.dirname(os.path.abspath(__file__))
    db_path: str = os.path.join(project_dir, 'db.sqlite3')

    settings_checks(db_path)
    extract_yatube_folder(project_dir)

    # copy db file
    db_destination_path = os.path.join(
        project_dir, YATUBE_FOLDER, 'db.sqlite3'
    )
    shutil.copyfile(db_path, db_destination_path)

    add_style_tag(project_dir)


def settings_checks(db_path: str):
    if not os.path.isdir(DOWNLOAD_FOLDER):
        raise Exception('Please set correct path to DOWNLOAD_FOLDER')

    if not os.path.exists(db_path):
        raise FileNotFoundError('Can\'t find db.sqlite3 file')


def extract_yatube_folder(project_dir: str):
    """Extract yatube folder from zip and remove zip from downloads."""
    download_files = glob.glob(f'{DOWNLOAD_FOLDER}*.zip')
    if download_files:
        archive_path = max(download_files, key=os.path.getctime)
    else:
        raise FileNotFoundError(
            'It seems there is no zip archive in Downloads'
        )

    extracted_obj_path = None

    archive = zipfile.ZipFile(archive_path)
    for archive_item in archive.namelist():
        if (os.sep + YATUBE_FOLDER + os.sep) in archive_item:
            extracted_obj_path = archive.extract(archive_item, project_dir)

    if extracted_obj_path is None:
        raise Exception('It looks like this is the wrong zip file')

    # remove old yatube dir
    old_yatube_dir = os.path.join(project_dir, YATUBE_FOLDER)
    if os.path.isdir(old_yatube_dir):
        shutil.rmtree(old_yatube_dir)

    # find a prefix of archive
    relative_archive_path = extracted_obj_path.replace(project_dir, '')
    extracted_dir = os.path.normpath(relative_archive_path)
    extracted_dir = extracted_dir.split(os.sep)
    prefix = extracted_dir[1]

    # copy folder with content
    yatube_from_archive_path = os.path.join(project_dir, prefix)
    copy_tree(yatube_from_archive_path, project_dir)
    shutil.rmtree(yatube_from_archive_path)

    if REMOVE_ZIP_FROM_DOWNLOADS:
        os.remove(archive_path)


def add_style_tag(project_dir: str):

    def find_base():
        for root, dirs, files in os.walk(project_dir):
            if 'base.html' in files:
                return os.path.join(root, 'base.html')

    base_path = find_base()
    with open(base_path) as f:
        s = f.read()
        if LOAD_STATIC_TAG not in s:
            raise Exception(f"Can't find {LOAD_STATIC_TAG}")

    with open(base_path, 'w') as f:
        s = s.replace(LOAD_STATIC_TAG,
                      LOAD_STATIC_TAG + '\n' + STYLE_TAG)
        f.write(s)


if __name__ == '__main__':
    main()

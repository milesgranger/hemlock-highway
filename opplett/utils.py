import s3fs
import os

from typing import Tuple, List
from opplett.models import UserModel, PaymentModel
from opplett.models import POSTGRES_DB


def create_tables():
    """
    Debug helper method: All setup goes here.
    """
    POSTGRES_DB.connect()
    POSTGRES_DB.create_tables([UserModel, PaymentModel], safe=True)
    POSTGRES_DB.close()


def get_s3fs() -> s3fs.S3FileSystem:
    """
    Convenience method, Return connected s3fs object
    """
    fs = s3fs.S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                           secret=os.environ.get('AWS_SECRET_ACCESS_KEY')
                           )
    return fs


def list_files_and_folders(username, path='') -> Tuple[List[str], List[str]]:
    """
    Given username and option path, return file details.
    :returns - Tuple containing a list of folders, and list of files.
    """

    # Get s3 and list the files given username and path.
    fs = get_s3fs()
    files = fs.ls('{bucket}/{username}/{path}'.format(bucket=os.environ.get('S3_BUCKET'),
                                                      username=username,
                                                      path=path),
                  detail=True)

    # format the files with the name of the file and build a link to that file
    for file in files:
        file['Name'] = os.path.basename(file['Key'])
        file['LocalLink'] = file.get('Key').replace('{bucket}/{username}/'.format(bucket=os.environ.get('S3_BUCKET'),
                                                                                  username=username), '')

    # Sort the files by name and if it is a directory.
    folders_tmp = sorted([f for f in files if not f.get('Size') or f.get('StoargeClass') == 'DIRECTORY'],
                         key=lambda d: d.get('StorageClass'),
                         reverse=False)

    # Folders are listed twice, once as a directory, another as a file with Size of 0
    last_key, folders = None, []
    for folder in folders_tmp:
        # Ensure the folder isn't given twice, and the folder we're in now isn't listed as an option
        if folder.get('Key') != last_key and not folder.get('LocalLink') == path:
            folders.append(folder)
            last_key = folder.get('Key')

    # Remove directories from files, as specified by no size.
    files = sorted([file for file in files if file.get('Size')], key=lambda dic: dic.get('Size'))
    return folders, files


def build_bread_crumbs(path):
    """
    Build a list of lists which looks like [[basename_of_folder, path_to_folder], ...]
    In order where 0th element is path to user's home-page-components directory, next would be [folder1, username/folder1]
    :param path: The path to build crumbs for.
    """
    crumbs = []
    crumb_path = ''
    for crumb in path.split('/'):
        crumb_path += '{crumb}/'.format(crumb=crumb)
        crumbs.append([crumb, crumb_path])
    return crumbs

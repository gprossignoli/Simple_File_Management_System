import os
from collections import namedtuple
from hashlib import sha256
from os import stat

from flask import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from sfms import db
from sfms.files.models import File
from sfms import settings as st

Files = namedtuple('Files', ['title', 'creation_date', 'size', 'hash'])


class FileAlreadyExistsError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()


class FileNotExistsError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()


class FileInsertionError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()


class FileDeletionError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()


class FileService:
    @staticmethod
    def get_user_files(user_id: int) -> tuple[Files, ...]:
        def show_file_size(size_in_bytes):
            to_MB = 1 * (10 ** -6)
            to_KB = 1 * (10 ** -3)
            size = round(size_in_bytes*to_MB, 3)
            unit = " MB"
            if size < 1:
                size = round(size_in_bytes*to_KB, 3)
                unit = " KB"
                if size < 1:
                    size = size_in_bytes
                    unit = " B"
            return str(size) + unit
        query_rst = db.session.query(File).filter_by(owner_id=user_id).all()

        files = [Files(title=file.title, creation_date=file.time_created,
                       size=show_file_size(file.file_size), hash=file.file_hash) for file in query_rst]
        files.sort(key=lambda x: x.title)
        return tuple(files)

    @classmethod
    def create_file(cls, uploaded_file: FileStorage, user_id: int):
        filename = secure_filename(uploaded_file.filename)
        if db.session.query(File).filter_by(title=filename).first() is not None:
            raise FileAlreadyExistsError(filename)
        blob = uploaded_file.read()
        size = len(blob)
        f_hash = sha256(blob).hexdigest()
        # A way of transactional insert
        try:
            cls.__save_file_db(f_hash, filename, size, user_id)
        except Exception as e:
            st.logger.exception(e)
            raise FileInsertionError(filename)
        else:
            cls.__save_file_disk(uploaded_file, filename)
            db.session.commit()

    @classmethod
    def delete_file(cls, file: File):
        try:
            db.session.delete(file)
        except Exception as e:
            st.logger.exception(e)
            raise FileDeletionError(file.title)
        else:
            os.remove(os.path.join(st.FILES_DIR, file.title))
        db.session.commit()

    @classmethod
    def get_file_by_title(cls, filename: str) -> File:
        file = db.session.query(File).filter_by(title=filename).first()
        if file is None:
            raise FileNotExistsError(filename)
        return file

    @classmethod
    def __save_file_db(cls, f_hash: str, filename: str, size: int, user_id: int):
        file = File(title=filename, file_size=size, file_hash=f_hash, owner_id=user_id)
        db.session.add(file)

    @classmethod
    def __save_file_disk(cls, file: FileStorage, filename: str):
        path = os.path.join(st.FILES_DIR, filename)
        file.save(path)
        return path

    @classmethod
    def get_file_from_disk(cls, filename):
        if not os.path.exists(os.path.join(st.FILES_DIR, filename)):
            raise FileNotExistsError
        return send_from_directory(directory=st.FILES_DIR, filename=filename)



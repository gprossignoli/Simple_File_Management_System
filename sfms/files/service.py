import os
from collections import namedtuple
from hashlib import sha256

from flask import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from sfms import db
from sfms.files.models import File
from sfms.users.models import User
from sfms import settings as st

Files = namedtuple('Files', ['title', 'creation_date', 'size', 'hash'])
Files_admin = namedtuple('Files_admin', ['owner', 'title', 'creation_date', 'size', 'hash'])


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
    @classmethod
    def get_all_files(cls, current_page: int) -> tuple[tuple[Files_admin, ...], int, int]:
        query_rst = db.session.query(File).order_by(
            File.title.asc()
        ).paginate(current_page, per_page=st.FILES_PER_PAGE)

        files = [Files_admin(owner=db.session.query(User).get(file.owner_id).username, title=file.title, creation_date=file.time_created,
                             size=cls.__show_file_size(file.file_size), hash=file.file_hash) for file in query_rst.items]

        next_page, prev_page = cls.__get_next_and_prev_page(has_prev=query_rst.has_prev,
                                                            has_next=query_rst.has_next,
                                                            current_page=current_page)

        return tuple(files), prev_page, next_page

    @classmethod
    def get_user_files(cls, user_id: int, current_page: int) -> tuple[tuple[Files, ...], int, int]:
        query_rst = db.session.query(File).filter_by(owner_id=user_id).order_by(
            File.title.asc()
        ).paginate(current_page, per_page=st.FILES_PER_PAGE)

        files = [Files(title=file.title[2:], creation_date=file.time_created,
                       size=cls.__show_file_size(file.file_size), hash=file.file_hash) for file in query_rst.items]

        next_page, prev_page = cls.__get_next_and_prev_page(has_prev=query_rst.has_prev,
                                                            has_next=query_rst.has_next,
                                                            current_page=current_page)

        return tuple(files), prev_page, next_page

    @classmethod
    def create_file(cls, uploaded_file: FileStorage, user_id: int):
        filename = secure_filename(f'{user_id}_{uploaded_file.filename}')
        if db.session.query(File).filter_by(owner_id=user_id, title=filename).first() is not None:
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

    @staticmethod
    def __show_file_size(size_in_bytes: int):
        to_MB = 1 * (10 ** -6)
        to_KB = 1 * (10 ** -3)
        size = round(size_in_bytes * to_MB, 3)
        unit = " MB"
        if size < 1:
            size = round(size_in_bytes * to_KB, 3)
            unit = " KB"
            if size < 1:
                size = size_in_bytes
                unit = " B"
        return str(size) + unit

    @staticmethod
    def __get_next_and_prev_page(has_prev: bool, has_next: bool, current_page: int) -> tuple[int,int]:
        if not has_prev:
            prev = current_page
        else:
            prev = current_page - 1
        if not has_next:
            next_p = current_page
        else:
            next_p = current_page + 1
        return next_p, prev


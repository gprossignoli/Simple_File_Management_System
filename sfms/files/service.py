from collections import namedtuple
from hashlib import sha256
from os import stat

from werkzeug.utils import secure_filename

from sfms import db
from sfms.files.models import File

Files = namedtuple('Files', ['title', 'creation_date', 'size', 'hash'])


class FileService:
    @staticmethod
    def get_user_files(user_id: int) -> tuple[Files, ...]:
        files_data = db.session.query(File).filter_by(owner_id=user_id).all()
        files = tuple([Files(*file_data) for file_data in files_data])
        return files

    @classmethod
    def create_file(cls, file):
        filename = secure_filename(file.title)
        size = stat(file).st_size
        f_hash = sha256(file)
        cls.__save_file_db(f_hash, filename, size)
        cls.__save_file_os(file)

    @classmethod
    def __save_file_db(cls, f_hash, filename, size):
        file = File(title=filename, file_size=size, file_hash=f_hash)
        db.session.add(file)
        db.session.commit()

    @classmethod
    def __save_file_os(cls, file):
        pass

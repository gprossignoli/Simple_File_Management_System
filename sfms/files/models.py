from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sfms import db


class File(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False, unique=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    file_size = Column(Integer(), nullable=False)
    file_hash = Column(String(256), nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'))

from sqlalchemy import Column, Integer, String, Boolean, func, Table, Float, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

photo_tag_table = Table(
    'photo_tag', Base.metadata,
    Column('photo_id', Integer, ForeignKey('photos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String, default="user")
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

    # Relacja do komentarzy
    comments = relationship("Comment", back_populates="user")
    photos = relationship("Photo", back_populates="user")

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    description = Column(String)
    tags = relationship("Tag", secondary=photo_tag_table)
    created_at = Column(DateTime, server_default=func.now())
    rating = Column(Float, default=0.0)  # Dodanie kolumny rating

    # Relacje do użytkownika i komentarzy
    user = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo", cascade="all, delete")

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacje do użytkownika i zdjęcia
    user = relationship("User", back_populates="comments")
    photo = relationship("Photo", back_populates="comments")


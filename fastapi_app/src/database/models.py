from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint
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
    """Class which describes table in database of the User
    :param id:int: User unique id in DB
    :param username: str: Username
    :param email: str: mail address of the user
    :param password: str: user password
    :param role: str: user role: admin, moderator or standard user
    :param created_at: datetime: the date of user creation
    :param avatar: str: link to the image of avatar in Cloudinary
    :param refresh_token: str: refresh_token of the user
    :param confirmed: boolean: information if the user is confirmed by mail
    """
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

class Image(Base):
    """Class which describes table in database of the Image
    :param id:int: image unique id in DB
    :param image_name: str: name of the image which is putting in DB
    :param image_link: link to the image
    :param created_at: date: the date of the image creation - format: YYYY-MM-DD HH:MM:SS where Y-means year, M - means month, D- means day H - means hour, M - means minutes and S - means seconds
    :param updated_at: date: the date of the image updating - format: YYYY-MM-DD HH:MM:SS where Y-means year, M - means month, D- means day H - means hour, M - means minutes and S - means seconds
    :param user_id: int: id number of the user who entered the image into the DB
    :param tags: tags about the image which is putting in DB. Relation 'many to many' - many tags to one images and one tag to many images.
    :param notes: the comment about the image which is putting in DB. Relation 'many to one' - many comments to one image.
    """
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String(50), nullable=False)
    image_link = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None, onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images")
    notes = relationship('Note', backref='images')
    opinions = relationship("Opinion", backref="image")

class Tag(Base):
    """
    Class which describes table in database of the Tag
    :param id: int: tag's unique id in DB
    :param name: str: tag's name
    :param user_id: int: id number of the user who entered the tag into the DB
    """
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class Comment(Base):
    """Class which describes table in database of the Comment
    :param id:int: comment's unique id in DB
    :param photo_id: the id number of the photo to which the tag is to be assigned
    :param user_id: int: Id number of the user who entered the note into the DB
    :param content: str: comment of the photo
    :param created_at: datetime: comment creation date
    :param updated_at: datetime: comment update date
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Opinion(Base):
    """
    Class which archives all opinion about photos
    :param id: int: opinion's unique id in DB
    :param vote: int: number of stars which show how the photo user loved
    :param user_id: int: id number of the user who voted
    :param photo_id: photo unique id in DB
    """
    __tablename__ = "opinions"
    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"))
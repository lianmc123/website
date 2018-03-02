import shortuuid
from exts import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3

class FrontUser(db.Model):
    __tablename__ = "front_user"
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    uid = db.Column(db.String(100), unique=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(20))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.SECRET)
    join_time = db.Column(db.DATETIME, default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get("password")
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)


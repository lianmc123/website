from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPermission(object):
    ALL_PERMISSION = 0b11111111  # 所有权限
    VISITOR = 0b00000001  # 访问者
    POSTER = 0b00000010  # 帖子管理
    COMMENTER = 0b00000100  # 评论管理
    BOARDER = 0b00001000  # 板块管理
    FRONTUSER = 0b00010000  # 前台用户管理
    CMSUSER = 0b00100000  # 后台用户管理
    ADMINER = 0b01000000  # 可以管理后台管理员


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_rold_id', db.INTEGER, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.INTEGER, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    permissions = db.Column(db.INTEGER, default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref="roles")


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DATETIME, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self._password, raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permission = role.permissions
            all_permissions |= permission
        return all_permissions

    def has_permission(self, permission):
        all_permission = self.permissions
        return all_permission & permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)

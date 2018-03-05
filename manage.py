from flask_script import Manager
from website import app
from flask_migrate import Migrate, MigrateCommand
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.common import models as common_models

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = cms_models.CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')


@manager.command
def create_role():
    visitor = cms_models.CMSRole(name="访客", desc="只能看相关数据,不能改")
    visitor.permissions = cms_models.CMSPermission.VISITOR
    operator = cms_models.CMSRole(name="运营", desc="能管理帖子,评论,前台用户")
    operator.permissions = cms_models.CMSPermission.VISITOR | cms_models.CMSPermission.POSTER \
                           | cms_models.CMSPermission.COMMENTER | cms_models.CMSPermission.FRONTUSER
    admin = cms_models.CMSRole(name="管理员", desc="拥有大部分权限")
    admin.permissions = cms_models.CMSPermission.VISITOR | cms_models.CMSPermission.POSTER \
                        | cms_models.CMSPermission.COMMENTER | cms_models.CMSPermission.FRONTUSER \
                        | cms_models.CMSPermission.CMSUSER | cms_models.CMSPermission.BOARDER
    developer = cms_models.CMSRole(name="终极管理员", desc="终极管理员,为所欲为")
    developer.permissions = cms_models.CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-r', '--role', dest='role')
def add_user_to_role(email, role):
    user = cms_models.CMSUser.query.filter_by(email=email).first()
    if user:
        role = cms_models.CMSRole.query.filter_by(name=role).first()
        if role:
            user.roles.append(role)
            db.session.commit()
            print("添加成功")
        else:
            print("找不到该角色")
    else:
        print("找不到该用户")


@manager.command
def test_permission():
    user = cms_models.CMSUser.query.first()
    if user.is_developer:
        print("有权限")
    else:
        print("没有权限")


@manager.option('-t', "--telephone", dest="telephone")
@manager.option('-u', "--username", dest="username")
@manager.option('-p', "--password", dest="password")
def create_front_user(telephone, username, password):
    front_user = front_models.FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(front_user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

from exts import db
from datetime import datetime


class BannerModel(db.Model):
    __tablename__ = "banner"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.INTEGER, default=0)
    is_show = db.Column(db.INTEGER, default=0)
    create_time = db.Column(db.DATETIME, default=datetime.now)

from sqlalchemy import inspect

from .. import db # from __init__.py

class Hostname(db.Model):
    __tablename__ = 'hostnames'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(4), nullable=False)
    postfix = db.Column(db.String(4), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Relations:
    macs = db.relationship('Mac', back_populates='hostname')
    descriptions = db.relationship('Description', back_populates='hostname')

    def __init__(self, prefix, postfix=None, description=None):
        self.prefix = prefix
        self.postfix = postfix
        self.description = description

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'<Hostname({self.prefix!r}, {self.id!r}, {self.postfix!r}, {self.description!r})>'

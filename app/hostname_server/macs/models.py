from sqlalchemy import inspect

from .. import db # from __init__.py


class Mac(db.Model):
    __tablename__ = 'macs'
    mac_str = db.Column(db.String(17), nullable=False, unique=True)
    mac_int = db.Column(db.BigInteger, nullable=False, unique=True, primary_key=True, autoincrement=False)
    
    # Relations:
    hostname_id = db.Column(db.Integer, db.ForeignKey('hostnames.id', ondelete='RESTRICT'))
    hostname = db.relationship('Hostname', back_populates='macs')

    def __init__(self, mac_str, mac_int, hostname_id):
        self.mac_str = mac_str
        self.mac_int = mac_int
        self.hostname_id = hostname_id

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'<Mac({self.mac_str!r}, {self.mac_int!r}, {self.hostname_id!r})>'

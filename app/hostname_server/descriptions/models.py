from sqlalchemy import inspect

from .. import db # from __init__.py

class Description(db.Model):
    # This table is for logging host descriptions for history purposes
    __tablename__ = 'descriptions'
    __table_args__ = (db.UniqueConstraint('text', 'client', 'hostname_id', name='uq_description'),)
    
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    client = db.Column(db.String(4), nullable=False)

    # Relations:
    hostname_id = db.Column(db.Integer, db.ForeignKey('hostnames.id', ondelete='RESTRICT'), nullable=False)
    hostname = db.relationship('Hostname', back_populates='descriptions')

    def __init__(self, text, client, hostname_id):
        self.text = text
        self.client = client
        self.hostname_id = hostname_id

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'<Description({self.text!r}, {self.client!r}, {self.hostname_id!r})>'

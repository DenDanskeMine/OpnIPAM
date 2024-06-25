from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Subnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cidr = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('subnet.id', ondelete='CASCADE'))
    children = db.relationship('Subnet', backref=db.backref('parent', remote_side=[id]))

class IPAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    subnet_id = db.Column(db.Integer, db.ForeignKey('subnet.id', ondelete='CASCADE'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=False)
    hostname = db.Column(db.String(100))
    mac_address = db.Column(db.String(50))
    rack = db.Column(db.String(50))
    device = db.Column(db.String(50))
    port = db.Column(db.String(50))
    os = db.Column(db.String(50))
    last_user = db.Column(db.String(50))
    last_seen = db.Column(db.DateTime)
    subnet = db.relationship('Subnet', backref=db.backref('ips', lazy=True))

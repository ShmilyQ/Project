from app import db
from datetime import datetime

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    contact_person = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联库位
    locations = db.relationship('Location', backref='warehouse', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'address': self.address,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100))
    zone = db.Column(db.String(20))  # 区域
    aisle = db.Column(db.String(10))  # 通道
    shelf = db.Column(db.String(10))  # 货架
    level = db.Column(db.String(10))  # 层级
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'warehouse_id': self.warehouse_id,
            'code': self.code,
            'name': self.name,
            'zone': self.zone,
            'aisle': self.aisle,
            'shelf': self.shelf,
            'level': self.level,
            'is_active': self.is_active
        }
from app import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventories'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    quantity = db.Column(db.Integer, default=0)
    reserved_quantity = db.Column(db.Integer, default=0)  # 预留数量
    available_quantity = db.Column(db.Integer, default=0)  # 可用数量
    batch_number = db.Column(db.String(50))  # 批次号
    expiry_date = db.Column(db.Date)  # 过期日期
    unit_cost = db.Column(db.Numeric(10, 2))  # 单价
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'location_id': self.location_id,
            'quantity': self.quantity,
            'reserved_quantity': self.reserved_quantity,
            'available_quantity': self.available_quantity,
            'batch_number': self.batch_number,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'updated_at': self.updated_at.isoformat()
        }
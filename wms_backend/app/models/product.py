from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    unit = db.Column(db.String(20), default='件')  # 单位
    weight = db.Column(db.Numeric(10, 3))  # 重量
    dimensions = db.Column(db.String(50))  # 尺寸 长x宽x高
    min_stock = db.Column(db.Integer, default=0)  # 最小库存
    max_stock = db.Column(db.Integer, default=0)  # 最大库存
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联库存
    inventories = db.relationship('Inventory', backref='product', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'unit': self.unit,
            'weight': float(self.weight) if self.weight else None,
            'dimensions': self.dimensions,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关联商品
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'description': self.description,
            'is_active': self.is_active
        }
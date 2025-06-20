from flask import Blueprint, request, jsonify
from app.models.warehouse import Warehouse
from app import db

bp = Blueprint('warehouse', __name__, url_prefix='/api/warehouse')

# 只保留分页和搜索的 GET 路由
@bp.route('', methods=['GET'])
def list_warehouses():
    # 获取分页参数
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    name = request.args.get('name', default='', type=str)
    code = request.args.get('code', default='', type=str)
    query = Warehouse.query
    if name:
        query = query.filter(Warehouse.name.like(f"%{name}%"))
    if code:
        query = query.filter(Warehouse.code.like(f"%{code}%"))
    pagination = query.order_by(Warehouse.id.desc()).paginate(page=page, per_page=size, error_out=False)
    warehouses = [w.to_dict() for w in pagination.items]
    return jsonify({
        'items': warehouses,
        'total': pagination.total,
        'page': pagination.page,
        'size': pagination.per_page
    })

@bp.route('', methods=['POST'])
def add_warehouse():
    data = request.json
    try:
        if not data.get('code') or not data.get('name'):
            return jsonify({'error': '仓库编码和名称不能为空'}), 400
        # 检查编码唯一性
        if Warehouse.query.filter_by(code=data.get('code')).first():
            return jsonify({'error': '仓库编码已存在'}), 400
        warehouse = Warehouse(
            code=data.get('code'),
            name=data.get('name'),
            address=data.get('address'),
            contact_person=data.get('contact_person'),
            contact_phone=data.get('contact_phone'),
            is_active=data.get('is_active', True)
        )
        db.session.add(warehouse)
        db.session.commit()
        return jsonify(warehouse.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

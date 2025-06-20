from flask import Blueprint, jsonify

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/stats')
def stats():
    # 示例统计数据，可根据实际模型查询替换
    return jsonify({
        'user_count': 10,
        'warehouse_count': 3,
        'product_count': 50,
        'inventory_count': 200
    })

@bp.route('/inventory-chart')
def inventory_chart():
    # 示例库存图表数据
    return jsonify({
        'labels': ['仓库A', '仓库B', '仓库C'],
        'data': [120, 60, 20]
    })

@bp.route('/order-chart')
def order_chart():
    # 示例订单图表数据
    return jsonify({
        'labels': ['1月', '2月', '3月'],
        'data': [30, 45, 60]
    })

@bp.route('/recent-activities')
def recent_activities():
    # 示例最近活动数据
    return jsonify([
        {'type': '入库', 'user': 'admin', 'time': '2025-06-20 10:00'},
        {'type': '出库', 'user': 'user1', 'time': '2025-06-19 15:30'}
    ])

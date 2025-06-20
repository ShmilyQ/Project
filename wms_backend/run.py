from app import create_app, db
from app.models import user, warehouse, product, inventory

app = create_app()

# 自动插入初始账号
@app.before_first_request
def create_default_user():
    from app.models.user import User
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin', email='admin@example.com', is_admin=True)
        u.set_password('123456')
        db.session.add(u)
        db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': user.User,
        'Warehouse': warehouse.Warehouse,
        'Product': product.Product,
        'Inventory': inventory.Inventory
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # 注册蓝图
    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    from app.api.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    from app.api.warehouse import bp as warehouse_bp
    app.register_blueprint(warehouse_bp, url_prefix='/api/warehouse')
    # 其余蓝图暂未实现，已注释
    # from app.api.product import bp as product_bp
    # from app.api.inventory import bp as inventory_bp
    # from app.api.order import bp as order_bp
    # from app.api.report import bp as report_bp
    # app.register_blueprint(product_bp, url_prefix='/api/product')
    # app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    # app.register_blueprint(order_bp, url_prefix='/api/order')
    # app.register_blueprint(report_bp, url_prefix='/api/report')
    
    return app
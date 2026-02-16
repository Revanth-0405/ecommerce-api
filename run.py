from flask import Flask
from app.config import Config
from app.db import db

from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from app.routes.order_routes import order_bp
from app.routes.report_routes import report_bp

from app.middleware.logging_middleware import request_logger
from app.utils.error_handler import error_response


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    request_logger(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(report_bp)

    # ---------------- GLOBAL ERROR HANDLER ---------------- #

    @app.errorhandler(Exception)
    def handle_exception(e):
        return error_response(str(e), "SERVER500", 500)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


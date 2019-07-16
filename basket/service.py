from flask import Flask, make_response, jsonify

from basket.service_config import Config
from basket import service_routes


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object(Config)

    app.register_blueprint(service_routes.bp)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({'error': 'Internal Server error'}), 500)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    return app
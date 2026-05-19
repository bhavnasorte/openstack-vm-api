import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from app.routes.vm_routes import vm_bp

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

def create_app():
    app = Flask(__name__)

    app.register_blueprint(vm_bp, url_prefix="/api/v1")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"data": None, "error": "Route not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"data": None, "error": "Method not allowed"}), 405

    return app

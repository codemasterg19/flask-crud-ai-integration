from flask import Flask
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from routes.task_routes import task_bp
from routes.ai_task_routes import ai_task_bp

def create_app():
    app = Flask(__name__)

    # Registro de Blueprints
    app.register_blueprint(task_bp)
    app.register_blueprint(ai_task_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

from main import create_app
from routes.blueprint import blueprint


App = create_app()
# Register blueprint root path
App.register_blueprint(blueprint, url_prefix='/clinic')

if __name__ == '__main__':
    App.run(host='127.0.0.1', port=5000, debug=True)


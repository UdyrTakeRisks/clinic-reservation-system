from threading import Thread

from controllers.messaging.receive import getPatientMessages
from main import create_app
from routes.blueprint import blueprint
from os import environ

URL = environ.get('BACKEND_URL')
PORT = environ.get('BACKEND_SERVER_PORT')

print("BACKEND_URL: ", URL)
print("BACKEND_SERVER_PORT: ", PORT)

App = create_app()
# Register blueprint root path
App.register_blueprint(blueprint, url_prefix='/clinic')

if __name__ == '__main__':
    # Start consuming messages in a separate thread
    # thread = Thread(target=getPatientMessages)
    # thread.start()
    # getPatientMessages()
    # Run the Flask app
    # App.run(host='0.0.0.0', port=5000, debug=True)
    App.run(host=URL, port=PORT, debug=True)


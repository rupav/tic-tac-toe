from flask import Flask

app = Flask(__name__)

from api.routes.routes import mod

app.register_blueprint(routes.routes.mod)

if __name__ == '__main__':
    app.run(debug=True)

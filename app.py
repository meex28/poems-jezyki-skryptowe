from flask import Flask
from controllers import registerEndpoints

app = Flask(__name__)
registerEndpoints(app)

if __name__ == '__main__':
    app.run()

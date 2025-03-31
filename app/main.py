from flask import Flask, Blueprint, send_from_directory

app = Flask(__name__)

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

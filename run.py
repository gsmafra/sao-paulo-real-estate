from flask import Flask, render_template
from app.main import main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False)

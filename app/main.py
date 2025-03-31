import sqlite3
from functools import wraps

from flask import Flask, Blueprint, jsonify, render_template, request

app = Flask(__name__)
app.template_folder = "templates"

main_blueprint = Blueprint("main", __name__)


def handle_exceptions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        # pylint: disable=W0718
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return wrapper


@main_blueprint.route("/")
def index():
    return render_template("index.html")


def load_query(filepath):
    """Load the SQL template from a file."""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


@main_blueprint.route("/real-estate")
@handle_exceptions  # Wrap endpoint with error handling.
def get_real_estate():
    db_path = "data/final/real_estate_data.db"
    logradouro_search = request.args.get("search", "")
    numero_search = request.args.get("numero", "")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load the SQL template from an external file.
    sql_filepath = "app/query.sql"
    query = load_query(sql_filepath)

    cursor.execute(
        query,
        (logradouro_search, f"%{logradouro_search}%", numero_search, numero_search),
    )
    rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    conn.close()
    return jsonify(results)


app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

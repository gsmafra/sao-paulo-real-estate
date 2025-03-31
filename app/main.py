from flask import Flask, Blueprint, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Ensure Flask knows where to find the templates folder
app.template_folder = 'templates'

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    # Serve the HTML file in templates/index.html
    return render_template('index.html')

@main_blueprint.route('/real-estate')
def get_real_estate():
    # Path to the SQLite database
    db_path = 'data/final/real_estate_data.db'
    search = request.args.get("search", "")  # Get filter value if exists

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
            SELECT
                nome_do_logradouro,
                numero,
                cep,
                data_de_transacao,
                area_construida_m2,
                acc_iptu,
                valor_de_transacao_declarado_pelo_contribuinte
            FROM data
            WHERE (? = '' OR nome_do_logradouro LIKE ?)
            LIMIT 50
        """
        # When search is empty, the condition (? = '') is true.
        # Otherwise, we filter rows using a non‑exact match.
        cursor.execute(query, (search, f"%{search}%"))
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

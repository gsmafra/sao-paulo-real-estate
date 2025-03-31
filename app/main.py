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
    logradouro_search = request.args.get("search", "")
    numero_search = request.args.get("numero", "")

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
              AND (? = '' OR numero = ?)
            ORDER BY data_de_transacao DESC
            LIMIT 50
        """
        # Using the OR trick to enable/disable the filters:
        # - If a filter is empty, the condition (? = '') becomes true.
        # - Otherwise, it applies the filter (LIKE for logradouro and exact match for numero).
        cursor.execute(query, (logradouro_search, f"%{logradouro_search}%", numero_search, numero_search))
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

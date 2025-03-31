from flask import Flask, Blueprint, jsonify, render_template
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
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query the first 50 rows from the real estate table
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
            LIMIT 50
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert rows to a list of dictionaries
        results = [dict(zip(column_names, row)) for row in rows]

        # Close the connection
        conn.close()

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

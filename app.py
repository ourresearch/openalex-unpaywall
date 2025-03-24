import os
import json

from databricks import sql
from flask import Flask, jsonify

app = Flask(__name__)

DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
DATABRICKS_HTTP_PATH = os.getenv('DATABRICKS_HTTP_PATH')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

app.json.sort_keys = False

# routes

@app.route('/unpaywall/<path:doi>', methods=['GET'])
def get_unpaywall_record(doi):
    with sql.connect(
            server_hostname=DATABRICKS_HOST,
            http_path=DATABRICKS_HTTP_PATH,
            access_token=DATABRICKS_TOKEN,
    ) as connection:
        with connection.cursor() as cursor:
            query = "SELECT json_response FROM openalex.unpaywall.unpaywall WHERE doi = %s"
            cursor.execute(query, (doi,))
            row = cursor.fetchone()

            if row is None:
                return jsonify({"error": "Item not found"}), 404

            result = json.loads(row[0])
            return jsonify(result)


if __name__ == '__main__':
    app.run()
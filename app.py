import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import UnpaywallFromWalden

app = Flask(__name__)

OPENALEX_DB = os.getenv('OPENALEX_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = OPENALEX_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/<doi>', methods=['GET'])
def get_unpaywall_record(doi):
    record = db.session.query(UnpaywallFromWalden).filter_by(doi=doi).one_or_none()
    if not record:
        return jsonify({'error': 'DOI not found'}), 404
    result = record.to_dict()
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
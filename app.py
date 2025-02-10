import os
import json

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

OPENALEX_DB = os.getenv('OPENALEX_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = OPENALEX_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.sort_keys = False

db = SQLAlchemy(app)

# routes

@app.route('/unpaywall/<path:doi>', methods=['GET'])
def get_unpaywall_record(doi):
    record = db.session.query(UnpaywallFromWalden).filter_by(doi=doi).one_or_none()
    if not record:
        return jsonify({'error': 'DOI not found'}), 404
    result = record.to_dict()
    return jsonify(result)


# models

class UnpaywallFromWalden(db.Model):
    __table_args__ = {'schema': 'unpaywall'}
    __tablename__ = 'unpaywall_from_walden'

    doi = db.Column(db.String, primary_key=True)
    json_response = db.Column(db.String)
    def __repr__(self):
        return f"<UnpaywallFromWalden(doi='{self.doi}')>"

    def to_dict(self):
        """Convert model instance to dictionary."""
        return json.loads(self.json_response)


if __name__ == '__main__':
    app.run(debug=True)
import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

OPENALEX_DB = os.getenv('OPENALEX_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = OPENALEX_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# routes

@app.route('/<path:doi>', methods=['GET'])
def get_unpaywall_record(doi):
    record = db.session.query(UnpaywallFromWalden).filter_by(doi=doi).one_or_none()
    if not record:
        return jsonify({'error': 'DOI not found'}), 404
    result = record.to_dict()
    return jsonify(result)


# models

class UnpaywallFromWalden(db.Model):
    __schema__ = 'unpaywall'
    __tablename__ = 'unpaywall_from_walden'

    doi = db.Column(db.String, primary_key=True)
    doi_url = db.Column(db.String)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    is_paratext = db.Column(db.String)
    published_date = db.Column(db.String)
    year = db.Column(db.Integer)
    journal_name = db.Column(db.String)
    journal_issns = db.Column(db.String)
    journal_issn_l = db.Column(db.String)
    journal_is_oa = db.Column(db.Boolean)
    journal_is_in_doaj = db.Column(db.Boolean)
    publisher = db.Column(db.String)
    is_oa = db.Column(db.Boolean)
    oa_status = db.Column(db.String)
    has_repository_copy = db.Column(db.Boolean)
    best_oa_location = db.Column(db.JSON)
    first_oa_location = db.Column(db.JSON)
    oa_locations = db.Column(db.JSON)
    oa_locations_embargoed = db.Column(db.JSON)
    updated = db.Column(db.DateTime)
    data_standard = db.Column(db.Integer)
    z_authors = db.Column(db.JSON)

    def __repr__(self):
        return f"<UnpaywallFromWalden(doi='{self.doi}', title='{self.title}')>"

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'doi': self.doi,
            'doi_url': self.doi_url,
            'title': self.title,
            'genre': self.genre,
            'is_paratext': self.is_paratext,
            'published_date': self.published_date,
            'year': self.year,
            'journal_name': self.journal_name,
            'journal_issns': self.journal_issns,
            'journal_issn_l': self.journal_issn_l,
            'journal_is_oa': self.journal_is_oa,
            'journal_is_in_doaj': self.journal_is_in_doaj,
            'publisher': self.publisher,
            'is_oa': self.is_oa,
            'oa_status': self.oa_status,
            'has_repository_copy': self.has_repository_copy,
            'best_oa_location': self.best_oa_location,
            'first_oa_location': self.first_oa_location,
            'oa_locations': self.oa_locations,
            'oa_locations_embargoed': self.oa_locations_embargoed,
            'updated': self.updated.isoformat() if self.updated else None,
            'data_standard': self.data_standard,
            'z_authors': self.z_authors
        }


if __name__ == '__main__':
    app.run(debug=True)
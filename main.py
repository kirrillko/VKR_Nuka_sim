from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.String(50), nullable=False)
    simulator = db.Column(db.Integer, nullable=False)
    recommendation = db.Column(db.Integer, nullable=False)
    usability = db.Column(db.Integer, nullable=False)
    reactors = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'who': self.who,
            'simulator': self.simulator,
            'recommendation': self.recommendation,
            'usability': self.usability,
            'reactors': self.reactors.split(',') if self.reactors else [],
            'timestamp': self.timestamp.isoformat()
        }
@app.route("/")
def read_index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("head_about.html")

@app.route("/feedback")
def feedback():
    return render_template("head_feedback.html")

@app.route("/terms")
def terms():
    return render_template("head_terms.html")

@app.route("/sources")
def sources():
    return render_template("head_sources.html")

@app.route("/simulator")
def simulator():
    return render_template("simulator.html")


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    # Валидация данных
    required_fields = ['who', 'simulator', 'recommendation', 'usability']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        feedback = Feedback(
            who=data['who'],
            simulator=int(data['simulator']),
            recommendation=int(data['recommendation']),
            usability=int(data['usability']),
            reactors=data.get('reactors', '')
        )

        db.session.add(feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback saved successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

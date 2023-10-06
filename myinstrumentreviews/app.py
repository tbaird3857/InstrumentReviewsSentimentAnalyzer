from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize NLTK Sentiment Analyzer
sid = SentimentIntensityAnalyzer()

# Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instrument = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=True)

# Drop and recreate the database
with app.app_context():
    db.drop_all()
    db.create_all()

# Function to calculate sentiment score
def calculate_sentiment(review_text):
    return sid.polarity_scores(review_text)['compound']

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        instrument = request.form['instrument']
        review_text = request.form['review']
        sentiment_score = calculate_sentiment(review_text)
        new_review = Review(instrument=instrument, review=review_text, sentiment_score=sentiment_score)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('review_form.html')

@app.route('/view_database')
def view_database():
    reviews = Review.query.all()
    return render_template('view_database.html', reviews=reviews)

@app.route('/calculate_average_sentiment')
def calculate_average_sentiment(reviews):
    if not reviews:
        return None

    # Calculate the average sentiment score
    total_sentiment = sum(review.sentiment_score for review in reviews if review.sentiment_score is not None)
    average_sentiment = total_sentiment / len(reviews)
    
    return average_sentiment

@app.route('/')
def index():
    reviews = Review.query.all()
    average_sentiment = calculate_average_sentiment(reviews)
    return render_template('index.html', reviews=reviews, average_sentiment=average_sentiment)

if __name__ == '__main__':
    app.run(debug=True)

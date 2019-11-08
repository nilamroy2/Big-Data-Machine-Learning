from flask import Flask, render_template, flash, request, jsonify, abort
#from flask_wtf import FlaskForm
#from wtforms import Form, TextField, TextAreaField, SubmitField
#from wtforms.validators import DataRequired
import os
import joblib
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
#from models import db,DrugDB
#from config import SQLALCHEMY_DATABASE_URI
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import Session, exc
#from sqlalchemy import create_engine, func
#import pandas as pd
import os


# App config.
app = Flask(__name__, static_url_path= "/static", static_folder="static")

#db.init_app(app)
###########################
# Database Setup
###########################


#app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)



###
## Function to test a new review and provide a sentiment
###

def check_review(test_review):
    print(test_review)
    result = model.predict(vectorizer.transform(test_review))
    result = result[0]
    
    return result

def check_review_api(test_review):
    result = model.predict(vectorizer.transform(test_review))
    print(type(result))
    print(result[0])
    if result[0]==1:
        outcome = "Seems the user is happy with the review!"
    else:
        outcome = "Seems the user had a bad experience with the drug!"
    
    response = {
        'prediction': f"{result}",
        'Outcome': outcome
    }

    return response

#class ReviewForm(FlaskForm):
#    review = TextField('review', validators=[DataRequired()])

@app.before_first_request
def setup():
    ## Loading model and vectorizer
    try:
      global model, vectorizer
      print("Model is loading.. Please be patient!!")
      filename = "vectorizer.sav"
      vectorizer = joblib.load(os.path.join("static/models", filename))

      filename = "drugML.sav"
      model = joblib.load(os.path.join("static/models", filename))
      
      
      print("Model has been successfully loaded!")

    except Exception as e:
      print("Model loading failed! ,Please check the console logs.")

@app.route('/')
def index():
    try:
          return render_template('index.html')
    except:

          abort(404)

@app.route('/form')
def home():
    """Return the homepage"""
    try:
       #form = ReviewForm()
       #if form.validate_on_submit():
       #     print(f"<h1>Review submitted is {form.review.data}")
       #     review_string = [form.review.data]
       #
       #    check_review(review_string)
       #    flash(check_review( review_string))
       return render_template('home.html')
    except:
        abort(404)

@app.route('/predict', methods=['POST'])
def predict():
    try:
       if request.method == 'POST':
           message = request.form['message']
           review_string = [message]
           my_prediction = check_review(review_string)
           print(f"Prediction is {my_prediction}")
       return render_template('result.html', prediction = my_prediction)
    except:
        abort(404)
    

@app.route("/api/v1.0/<_string>", methods=['GET'])
def api(_string):
    try:
        review_string = [_string]
        print(review_string)
        return jsonify(check_review_api(review_string))
    except:
        
        abort(404)

@app.route("/process")
def process():
    try:        
        return render_template("process.html", image_name = "img/methodology.png")
    except:
        abort(404)

@app.route("/ml_process")
def ml_process():
    try:
        return render_template("ml_process.html", image_name= "img/process_flow.png")
    except:
        abort(404)

@app.route("/data")
def data():
     try:        
        return render_template("data.html", image_name = "img/data.png")
     except:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404 

if __name__ == "__main__":
    app.run(debug=True)
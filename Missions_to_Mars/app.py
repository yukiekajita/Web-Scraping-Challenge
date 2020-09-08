from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__, template_folder='templates')

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():
    mars_dict = mongo.db.collection.find_one()
    return render_template("index.html", mars = mars_dict)


@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_all()

    # Update the Mongo Database
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

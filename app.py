from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)


@app.route("/")
def index():
    # statement that finds all the items in the db and sets it to a variable
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars

    # calls the scrape function
    mars_master = mission_to_mars.scrape()

    #updates the database
    mars.update({}, mars_master, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

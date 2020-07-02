from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from pprint import PrettyPrinter as pprinter
import collections  # From Python standard library.
# import bson
# from bson.codec_options import CodecOptions

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo =PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")
#pp = pprinter(indent=4)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
import os

import pandas as pd
import numpy as np
import requests
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

params = {
    'battlenetkey': 'a4fa6e85904f40e78394a227ebf890dc',
    'clientsecret': 'QaeU3BTncNNGfk6Ht8rGDGhDrd4qMSbd'
  }
  
    
@app.route("/")
def index():
    """Return the homepage."""
    
    r = requests.get(
      'https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token=USaCJz7ZJKLECVr0F7lD7rrMIlYnGBjPs8',
      params=params)
    print(r.json())
    df = pd.DataFrame(r.json()['character_specializations'])
    print(df.head())

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/realms")
def names():
 
    return jsonify()

"""
#@app.route("/metadata/<sample>")
#def sample_metadata(sample):
 #Return the MetaData for a given sample.
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    #Return `otu_ids`, `otu_labels`,and `sample_values`.
    print(db.session)
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)
    """


import json
import os
import sys

import numpy as np
import pandas as pd
import requests
from rauth import OAuth2Service
from flask import Flask, Response, redirect, url_for, render_template, jsonify, session, request
#can get rid of sqlalchemy if we dont implement any database storage
from flask_sqlalchemy import SQLAlchemy
#our own file imports
from dicts import classdicts, specdicts, racedicts
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.debug = True
app.env='development'
app.config['SECRET_KEY']= os.urandom(24)
tokens = {}
client_id = 'a16a3fea45be4352916f9975f11b6803'
client_secret = 'BtCHX7vGo2p7OSCQva70QN7GUCIme8pA'
redirect_uri = 'http://127.0.0.1:5000/callback'
oauth = OAuth2Service(name='oauth', client_id=client_id, client_secret=client_secret, access_token_url='https://us.battle.net/oauth/token',
                    authorize_url='https://us.battle.net/oauth/authorize', base_url='https://us.battle.net/')
#to pass objects between routes.
class DataStore():
    a = None
    b = None
    c = None
data = DataStore()


@app.route('/')
def index():
    tokens['community'] = get_community_token()
    return(render_template('index.html', classdicts=list(classdicts.values()),
    racedicts=list(racedicts.values()), specdicts=list(specdicts.values())))

@app.route('/leaderboard')
def leaderboard():
    print('leaderboard function')
    print(tokens['community'])
    resp = requests.get(f"https://us.api.blizzard.com/wow/leaderboard/3v3?locale=en_US&access_token={tokens['community']}").json()
    df = pd.DataFrame(resp['rows'])
    df.classId = [classdicts[x] for x in df.classId]
    df.raceId = [racedicts[x] for x in df.raceId]
    df.specId = [specdicts[x] for x in df.specId]
    json_data = df.to_json(orient='records') 
    data.a = df  
    return(json_data)

@app.route('/filter')
def filter():
    print('in filter route')
    df = data.a
    if request.args.get('allclasses'):
        count = df.groupby(['classId']).size()
        countdict = count.to_json()
        return(countdict)
    if request.args.get('specfilter'):
        specfilter=request.args.get('specfilter')
        return(specfilter)
    if request.args.get('racefilter'):
        racefilter=request.args.get('racefilter')
        return(racefilter)
    if request.args.get('classfilter'):
        classfilter=request.args.get('classfilter')
        df = data.a
        filteredDF = df.loc[df['classId'] == classfilter]
        count = filteredDF.groupby(['raceId']).size()
        countdict = count.to_json()
        return(countdict)
    
def get_community_token():
    data2 = {'grant_type': 'client_credentials'}
    resp = oauth.get_access_token(data=data2, decoder=json.loads)
    print('COMMUNITY TOKEN:' + resp)
    return(resp)

if __name__ == "__main__":
    app.run(debug=True)  
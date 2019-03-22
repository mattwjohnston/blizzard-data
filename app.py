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
    api_connect() #we only need this call if we want the community token a bit faster.  if we dont call it, leaderboard doesnt have it when its called.  Need to delay the leaderboard till this variable is filled
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
    

@app.route('/api_connect')
def api_connect():
    # There are two types of tokens.  session['community_token'] and session['profile_token']
    # This route runs automatically at the homepage. the app.js file calls it.
    tokens['community'] = get_community_token()
    return(redirect(get_profile_authorization()))

@app.route('/callback', methods=["GET"])
def callback():
    return(get_profile_token())

def get_community_token():
    data2 = {'grant_type': 'client_credentials'}
    resp = oauth.get_access_token(data=data2, decoder=json.loads)
    print('COMMUNITY TOKEN:' + resp)
    return(resp)

def get_profile_authorization():
    authorization_url = oauth.get_authorize_url(
        client_id=client_id,
        state='ca',
        scope='wow.profile',
        redirect_uri=redirect_uri,
        response_type='code')
    return(authorization_url)

def get_profile_token():
    code = request.args.get('code')
    data2 = {
        'redirect_uri':redirect_uri,
        'scope':'wow.profile',
        'grant_type':'authorization_code',
        'code':code}
    resp = oauth.get_access_token(data=data2, decoder=json.loads)
    tokens['profile'] = resp
    print('PROFILE TOKEN:' + tokens['profile'])
    return('',200)

if __name__ == "__main__":
    app.run(debug=True)  
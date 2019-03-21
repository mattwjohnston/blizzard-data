import json
import os

import numpy as np
import pandas as pd

import requests
from rauth import OAuth2Service
from flask import Flask, Response, redirect, url_for, render_template, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.env='development'
app.config['SECRET_KEY']= os.urandom(24)
tokens = {}
client_id = 'a16a3fea45be4352916f9975f11b6803'
client_secret = 'BtCHX7vGo2p7OSCQva70QN7GUCIme8pA'
redirect_uri = 'http://127.0.0.1:5000/callback'
oauth = OAuth2Service(name='oauth', client_id=client_id, client_secret=client_secret, access_token_url='https://us.battle.net/oauth/token',
                    authorize_url='https://us.battle.net/oauth/authorize', base_url='https://us.battle.net/')

@app.route('/')
def index():
    api_connect() #we only need this call if we want the community token a bit faster.  if we dont call it, leaderboard doesnt have it when its called.  Need to delay the leaderboard till this variable is filled
    return(render_template('index.html'))

@app.route('/leaderboard')
def leaderboard():
    print('leaderboard function')
    print(tokens['community'])
    #session = oauth.get_session(tokens['community']) --- we could do easier calls on a session but i could not get it working well in local environment
    resp = requests.get(f"https://us.api.blizzard.com/wow/leaderboard/3v3?locale=en_US&access_token={tokens['community']}").json()
    df = pd.DataFrame(resp['rows'])
    #print(df.to_json(orient='records')) #it works
    return(df.to_json(orient='records'))

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
        redirect_uri='http://127.0.0.1:5000/callback',
        response_type='code')
    return(authorization_url)

def get_profile_token():
    code = request.args.get('code')
    data2 = {
        'redirect_uri':'http://127.0.0.1:5000/callback',
        'scope':'wow.profile',
        'grant_type':'authorization_code',
        'code':code}
    resp = oauth.get_access_token(data=data2, decoder=json.loads)
    tokens['profile'] = resp
    print('PROFILE TOKEN:' + tokens['profile'])
    return('',200)

'''
def fetch_leaderboard(conn):
    print('leaderboard func')
    resp = requests.get('https://us.api.blizzard.com/wow/leaderboard/3v3?locale=en_US&access_token='+ session['community_token'])
    resp=conn.get('/wow/leaderboard/3v3', params={'format':'json'})
    print(resp.data.get_json())
    df = pd.DataFrame(resp['rows'])
    print(df.head())
    return(df.to_json(orient='records'))
'''

if __name__ == "__main__":
    app.run(debug=True)  
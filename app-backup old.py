import json
import os

import numpy as np
import pandas as pd
import requests

import sqlalchemy
from flask import (Flask, Response, jsonify, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

from werkzeug import security
from requests_oauthlib import OAuth2Session

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from config import Auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'blizzard': {
        'id': 'a16a3fea45be4352916f9975f11b6803',
        'secret': 'BtCHX7vGo2p7OSCQva70QN7GUCIme8pA',
    }
}


app.config.from_object(DefaultConfig)


token_uri = 'https://us.battle.net/oauth/token'
authorization_uri = 'https://us.battle.net/oauth/authorize'
redirect_path='https://localhost:5000/'
base_url= 'https://us.battle.net/'
scope = 'wow.profile'
scope2 = 'wow/profile'

oauth = OAuth(app)
blizzard = oauth.remote_app(
    'blizzard',
    consumer_key='a16a3fea45be4352916f9975f11b6803',
    consumer_secret='BtCHX7vGo2p7OSCQva70QN7GUCIme8pA',
    request_token_params={'grant_type':'client_credentials', 'redirect_uri':redirect_path, 'scope': scope, 'state': lambda: security.gen_salt(10)},
    base_url=base_url,
    request_token_url=None,
    access_token_method='POST',
    access_token_url=token_uri,
    authorize_url=authorization_uri,
    # force to parse the response in applcation/json
    content_type='application/json',
)

def new_decoder(payload):
    return json.loads(payload.decode('utf-8'))

@app.route('/')
def home():
    if blizzard_token():
        response = blizzard.get('/wow/leaderboard/3v3')
        return jsonify(response.data)
    return "<a href='%s'>Connect to Blizzard's Game Data</a>" % url_for('blizzard_connect')

@app.route('/blizzard/connect')
def blizzard_connect():
    results = blizzard.authorize(redirect_uri = url_for('blizzard_connect_callback', 
        next=request.args.get('next') or request.referrer or url_for('index')), _external=True)
    print(results)
    return(results)

@app.route('/blizzard/connect/callback')
@blizzard.authorized_handler
def blizzard_connect_callback():
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u"We are having trouble connecting to Blizzard's game data right now.")
        return redirect(next_url)
    session['access_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['state'] = resp['state']

    return redirect(next_url)

@blizzard.tokengetter
def blizzard_token():
    return session.get('access_token')

app.secret_key = os.urandom(24)
if __name__ == "__main__":
    app.run(debug=True,  ssl_context='adhoc')  


'''   
@app.route("/")
def index():
    if 'access_token' in session:
        connection = blizzard.get('access_token')
        return jsonify(connection.data)
    return redirect(url_for('connect_to_blizzard'))

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/blizzard_connection")
def blizzard_connection():
    oauth.init_app(app)
    return redirect(authorization_uri)

def connect_to_blizzard():
    return blizzard.authorize_url(callback=url_for('home', _external=True))

@app.route("/api-connected")
def api_connected():
    resp = blizzard.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['access_token'] = (resp['access_token'], '')
    auth = blizzard.get('auth')
    return jsonify(auth.data)

@blizzard.tokengetter
def get_blizzard_access_token():
    return session.get('access_token')

@app.route('/callback?<access_code>')
def callback():
    assert 'error' not in request.args, request.args

    # in the real world we should validate that `state` matches the state we set before redirecting the user
    state = request.args.get('state')

    # using the code we've just been given, make a request to obtain
    # an access token for this user
    code = request.args.get('code')
    response = requests.post("https://us.battle.net" + '/oauth/token/', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret
    })
    assert response.ok, 'Token request failed: %s' % response.content

    data = response.json()
    token = data['access_token']
    headers = {
        'Authorization': 'Bearer %s' % token,
    }
    return headers


if __name__ == "__main__":
    app.run(debug=True,  ssl_context='adhoc')  
'''

'''
@app.route("/fetch_data")
def fetch_data():
    print('fetchdata 1 starting')

    wow = OAuth2Session(client_id, client_secret, authorization_uri, token=Response(request.token_from_fragment())
    
    params={'grant_type': 'client_credentials',
            'scope': scope,
            'state': 'foo',
            'redirect_uri': redirect_path,
            'response_type': 'code'
            }
    authorization_url, state = wow.authorization_url(**params)
    redirect_response = raw_input(authorization_url)
    oauth_response = oauth.parse_authorization_response(redirect_response)

    print(authorization_url)
    session['oauth_state'] = state
  #redirect_response = raw_input(authorization_url)
   # wow.token_from_fragment(redirect_response)

    return redirect(authorization_url)

@app.route('/callback?<access_code>')
def callback():
    assert 'error' not in request.args, request.args

    # in the real world we should validate that `state` matches the state we set before redirecting the user
    state = request.args.get('state')

    # using the code we've just been given, make a request to obtain
    # an access token for this user
    code = request.args.get('code')
    response = requests.post("https://us.battle.net" + '/oauth/token/', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret
    })
    assert response.ok, 'Token request failed: %s' % response.content

    data = response.json()
    token = data['access_token']
    headers = {
        'Authorization': 'Bearer %s' % token,
    }
    return headers


if __name__ == "__main__":
    app.run(debug=True,  ssl_context='adhoc')    
    
    

  


    wow = OAuth2Session(client_id, client_secret,
            token_updater=token_uri,
            state=session['oauth_state'])  
    token = wow.fetch_token(redirect_uri=redirect_url, grant_type='authorization_code', code=r.code, scope="wow.profile")
    return(token)


    print('fetch data 1 ending')
    print(authorization_url)
    params2 = {'grant_type':'authorization_code', 
            'scope':'wow.profile',
            'redirect_uri':"https://localhost:5000/callback",
            'code':'test'
            }

    session = wow.get_auth_session(data=params2, decoder=new_decoder)
    return (wow.get_auth_session(data=params2, decoder=new_decoder))


app.secret_key = os.urandom(24)
if __name__ == "__main__":
    app.run(debug=True,  ssl_context='adhoc')

    
    
    
    
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    code = dict(parse_qsl(get_args))
    print(code)


    params2 = {
            'grant_type':'authorization_code', 
            'scope':'wow.profile',
            'redirect_uri':"https://localhost:5000",
            'code':'test'
            }
    access_token = wow.get_access_token(data=params2, decoder=json.loads)

    for each in access_token:
        print(each)
    return(access_token)
    #access_token = wow.get_raw_access_token(url, data=params)

    # once the above URL is consumed by a client we can ask for an access
    # token. note that the code is retrieved from the redirect URL above,
    # as set by the provider
    print(access_token)
    data = {'response_type': 'code',
            'grant_type':'authorization_code',
            'redirect_uri': 'https://localhost:5000',
            'code':access_token}

    session = wow.get_auth_session(data=data)

    r = session.get('/wow/leaderboard/3v3')
    



    params = {'code':'bar', 'grant_type':'client_credentials', 'redirect_uri':'https://localhost:5000/'}
    access_token = wow.get_access_token(data=params, decoder=json.loads)
    resp = requests.get('https://us.api.blizzard.com/wow/leaderboard/3v3?locale=en_US&access_token='+access_token)


    df = pd.DataFrame(resp.json()['rows'])
    #classCounts = df.groupby(['classId']).size().to_dict()
    session = wow.get_auth_session(request_token,request_token_secret,method='POST',data={'oauth_verifier': pin})



    return df.to_json(orient='records')

    

@app.route("/pvedata")
def pvedata():
    resp = requests.get('https://us.api.blizzard.com/wow/leaderboard/3v3?locale=en_US&access_token=USd6CJcCUAFjnKm61RRYE9eu287xuQQDqG')
    df = pd.DataFrame(resp.json()['rows'])
    classCounts = df.groupby(['classId']).size().to_dict()
    print(classCounts)


    return jsonify(classCounts)



#app.secret_key = os.urandom(24)
if __name__ == "__main__":
    app.run(debug=True,  ssl_context='adhoc')




r = requests.get(
      'https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token=USaCJz7ZJKLECVr0F7lD7rrMIlYnGBjPs8',
      params=params)
    print(r.json())
    df = pd.DataFrame(r.json()['character_specializations'])
    print(df.head())

@app.route("/metadata/<sample>")
def sample_metadata(sample):
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
    '''

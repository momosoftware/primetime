# Standard Library
import base64
import configparser
import json
import logging
import os
import re
import smtplib
import sys
import time
import traceback
from datetime import date, datetime
 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

configparser = configparser.RawConfigParser()
configFilePath = r'config.conf'
configparser.read(configFilePath)

logger = logging.getLogger('primetime')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs/primetime.py.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - %(message)s','%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)

logger.addHandler(fh)

logger.debug('')
logger.debug('')
logger.debug('')
logger.info('=== Primetime Started ===')

logger.debug('Initializing Flask App')
# start our flask app and define endpoints
app = Flask(__name__)
app.secret_key = configparser.get('general', 'appSecret')
logger.info('Flask Initialized')

# Keys for providing OAuth
app.config['DISCORD_CLIENT_ID'] = configparser.getint('discord', 'client')
app.config['DISCORD_CLIENT_SECRET'] = configparser.get('discord', 'secret')
app.config['DISCORD_REDIRECT_URI'] = configparser.get('discord', 'callback')

# Checking guild/role applicability, effectivly handing off authentication to Discord
app.config['DISCORD_GUILD_ID'] = configparser.getint('discord', 'guild')
app.config['DISCORD_REQUIRE_ROLE'] = configparser.getboolean('discord', 'requireRole')
app.config['DISCORD_ROLE_ID'] = configparser.getint('discord', 'role')

app.config['STREAM_LOCATION'] = configparser.get('general', 'streamLocation')

discord = DiscordOAuth2Session(app)
logger.info('Discord Initialized')

@app.errorhandler(403)
def unauthorized(e):
	return 'go away :c (you\'re missing the requisite guild membership)', 403 # TODO this should be a template

@app.route('/')
@requires_authorization
def index():
	user = discord.fetch_user()
	logger.info('root!')
	# count += 1
	# session['count'] = count
	return render_template('index.html', user=user, streamLocation=app.config['STREAM_LOCATION'])

@app.route('/login/')
def login():
	return discord.create_session()

@app.route('/logout/')
@requires_authorization
def logout():
	discord.revoke()
	return 'You have logged out. <a href="{}">Click here</a> to go home and authenticate again'.format(url_for('index')), 200 # TODO make into an actual template

@app.route('/callback/')
def callback():
	discord.callback()
	user = discord.fetch_user()
	for guild in user.fetch_guilds():
		if guild.id == app.config['DISCORD_GUILD_ID']:
			# if ((app.config['DISCORD_REQUIRE_ROLE'] and app.config['DISCORD_ROLE_ID'] in user.roles)
			# or not app.config['DISCORD_REQUIRE_ROLE']):
			return redirect(url_for('index'))
	# if no servers matched, or we had a role requirement they couldnt fulfill
	discord.revoke()
	abort(403)


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
	return redirect(url_for('login'))

	
@app.route('/me/') # debug, turn into "profile" page later
@requires_authorization
def me():
	user = discord.fetch_user()
	return f'''
	<html>
		<head>
			<title>{user.name}</title>
		</head>
		<body>
			<img src='{user.avatar_url}' />
		</body>
	</html>'''


@app.route('/playlist', methods=['POST']) # placeholder, will handle playlist switching in the future
def charge():
	return jsonify({'yes': 'hello', 'no': 'goodbye'})

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

# Primetime
HTML5 video client utilizing video-js to connect to a HLS stream on the local server (or at least behind the same proxy/domain), locked behind Discord Auth that checks for Guild/Server membership before granting access

## Features
1. Discord Auth
2. VideoJS player
3. thats about it
4. really, it's just a video player locked behind discord auth

## Planned
1. PLaylist switching for multiple "channels"
2. "Up next" preview for streams
3. Discord channel chat mirroring
4. Deny login based on Discord Guild Role membership

## Installation
1. pip install -r requirements.txt
2. Run as a service and serve with nginx by following [these instructions from DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)

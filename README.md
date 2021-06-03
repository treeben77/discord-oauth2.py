# DiscordOAuth2.py
Use Discord's OAuth2 effortlessly! Turns the auth code to a access token and the access token into scope infomation.

### Using DiscordOAut2.py with Flask

```python
from flask import Flask, redirect, request
from threading import Thread
import discordoauth2 as oauth2
import os

app = Flask('')
oauth2.client({
  'client_id': '849<example>993044', #the client id for your application
  'client_secret': os.environ['oauth2_secret'], #the client secret for your application. Be super-extra-very-we-are-not-kidding-like-really-be-secure-make-sure-your-info-is-not-in-your-source-code careful with this.
  'redirect_uri': 'https://example.com/oauth2', #the redirect for the uri below
  'bot_token': os.environ['bot_token'] #the token for your app's bot, only required if you need to use guild.join
})

oauth2_uri = "https://discord.com/api/oauth2/authorize?client_id=849<example>993044&redirect_uri=https%3A%2F%2Fexample.com%2Foauth2&response_type=code&scope=identify"

@app.route('/oauth2')
def oauth():
  code = request.args.get('code')
  if not code:
    return redirect(oauth2_uri)
  else:
    token = oauth2.exchange_code(code)
    if str(token) == """{'error': 'invalid_request', 'error_description': 'Invalid "code" in request.'}""":
      return redirect(oauth2_uri)
    identify = oauth2.get_identify(token['access_token'])
    connections = oauth2.get_connections(token['access_token'])
    guilds = oauth2.get_guilds(token['access_token'])
    oauth2.join_guild(token['access_token'], 849912914450448395)
    return f'{identify}<br/><br/>{connections}<br/><br/>{guilds}'

def run():
  app.run(host="0.0.0.0", port=8080)

server = Thread(target=run)
server.start()
```

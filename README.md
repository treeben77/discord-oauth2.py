# DiscordOAuth2.py
Use Discord's OAuth2 effortlessly! Turns the auth code to a access token and the access token into scope infomation.

### Using DiscordOAuth2.py with Flask
```python
from flask import Flask, redirect, request
from threading import Thread
from discordoauth2 import discordOauth2
import os

app = Flask('Discord OAuth2 Example')
client = discordOauth2(client=159985870458322944, secret=os.environ['oauth2_secret'],
 redirect="https://example.com", token=os.environ['bot_token'])
#Replace the int above with your application's client ID and the redirect with the redirect URL with the redirect URL this flask hosts. add your oauth2 secret and bot token to a .env file.
#token could be None. token must be a valid Bot Token or None. Only required if your application adds users to a guild.

@app.route('/')
def main():
  return redirect("https://discord.com/api/oauth2/authorize?client_id=159985870458322944&redirect_uri=https%3A%2F%2Fexample.com%2Foauth2&response_type=code&scope=identify%20email%20connections%20guilds%20guilds.join")

@app.route('/oauth2')
def oauth():
  code = request.args.get('code')
  tokenObject = client.exchange_code(token=code)
  
  identify = tokenObject.identify()
  connections = tokenObject.connections()
  guilds = tokenObject.guilds()
  tokenObject.join_guild(336642139381301249)
  return f"{identify}<br/><br/>{connections}<br/><br/>{guilds}"

def run():
  app.run(host="0.0.0.0", port=8080)

server = Thread(target=run)
server.start()
```

# DiscordOAuth2.py
Use Discord's OAuth2 effortlessly! Turns the auth code to a access token and the access token into scope infomation.

> **Notice:** I don't know how to make my library work with `pip install` so you'll have to copy the source code and paste it into your workspace.

### Using DiscordOAuth2.py with Flask
You can try out a working example here: https://DiscordOAuth2py.treeben77.repl.co
```python
from flask import Flask, redirect, request
from discordoauth2 import discordOauth2
import os

app = Flask('Discord OAuth2 Example')
client = discordOauth2(client=your-client-id, secret="your-client-secret",
redirect="your-redirect-url", token="your-bot-token (optional)")
# Replace your-client-id with your application's client id, replace your-client-secret with your client secret and replace your-redirect-url with the url that discord will redirect users to once they complete OAuth2.
# If you want to add users to a guild, insert a bot token with CREATE_INSTANT_INVITE permissions in the guilds you want to add users to.

@app.route('/')
def main():
  # Your OAuth2 url, you can make one a https://discord.dev
  return redirect("https://discord.com/api/oauth2/authorize")

@app.route('/oauth2')
def oauth():
  tokenObject = client.exchange_code(token=request.args.get('code'))
  print("refresh token: "+tokenObject.refresh_token)
  
  # returns basic data about the user, including username, avatar and badges, if the email scope was parsed, it will also return their email.
  identify = tokenObject.access.identify()
  # returns visible and hidden connections such as GitHub, YouTube or Twitter.
  connections = tokenObject.access.connections()
  # returns a list of guilds that the user is in
  guilds = tokenObject.access.guilds()
  # returns a member object for the provided guild
  guilds_member = tokenObject.access.guilds_member(guilds[0]["id"])
  # makes a user join a guild, bot token provided must have CREATE_INSTANT_INVITE in that guild
  tokenObject.access.guilds_join(guild-id-here)

  return f"{identify}<br><br>{connections}<br><br>{guilds}<br><br>guild data for the first guild: {guilds_member}"

app.run(host="0.0.0.0", port=8080)
```

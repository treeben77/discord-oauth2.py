from flask import Flask, redirect, request
import discordoauth2
import os

app = Flask('Discord OAuth2 Example')
client = discordoauth2.Client(client=your-client-id, secret="your-client-secret",
redirect="your-redirect-url", token="your-bot-token (optional)")
# Replace your-client-id with your application's client id, replace your-client-secret with your client secret and replace your-redirect-url with the url that discord will redirect users to once they complete OAuth2.
# If you want to updated linked roles metadata or add users to a guild, insert a bot token with CREATE_INSTANT_INVITE permissions in the guilds you want to add users to.

client.update_linked_roles_metadata([
    {
        "type": 2,
        "key": "level",
        "name": "Level",
        "description": "The level the user is on"
    },
    {
        "type": 2,
        "key": "wins",
        "name": "Wins",
        "description": "The number of times the user has won"
    },
    {
        "type": 7,
        "key": "supporter",
        "name": "Supporter",
        "description": "Spent money to help the game"
    }
])

@app.route('/')
def main():
  # Your OAuth2 url, you can make one a https://discord.dev
  return redirect("https://discord.com/api/oauth2/authorize")

@app.route('/oauth2')
def oauth():
  access_token = client.exchange_code(token=request.args.get('code'))
  print("refresh token: "+access_token.refresh)
  
  # returns basic data about the user, including username, avatar and badges, if the email scope was parsed, it will also return their email.
  identify = access_token.fetch_identify()
  # returns visible and hidden connections such as GitHub, YouTube or Twitter.
  connections = access_token.fetch_connections()
  # returns a list of guilds that the user is in
  guilds = access_token.fetch_guilds()
  # returns a member object for the provided guild
  guilds_member = access_token.fetch_guild_member(guilds[0]["id"])
  # makes a user join a guild, bot token provided must have CREATE_INSTANT_INVITE in that guild
  access_token.join_guild(guild-id-here, identify["id"])
  # this update's the user's metadata for linked roles.
  access_token.update_metadata("Platform Name", "Username",  level=69, wins=420, supporter=True)
  # when you're done with the token, you can revoke it: note this revokes both the access token and refresh token.
  access_token.revoke()

  return f"{identify}<br><br>{connections}<br><br>{guilds}<br><br>guild data for the first guild: {guilds_member}"

app.run(host="0.0.0.0", port=8080)
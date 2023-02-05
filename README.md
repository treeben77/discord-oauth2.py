# DiscordOAuth2.py
Use Discord's OAuth2 effortlessly! Turns the auth code to a access token and the access token into scope infomation.

### Useful Links
Discord Server: https://discord.gg/DJ9xbbZAP5

Documentation is coming soon, don't worry.

## Quickstart
### Installing
I've finally published the library to PyPi! So now you can use pip.
```
pip install discord-oauth2.py
```
### Example With Flask
Don't forget to replace all the client information with your application's own information. You can leave bot token empty if your not adding members to guilds.
```py
import discordoauth2
from flask import Flask, request

client = discordoauth2.Client(849930878276993044, secret="very-secret-code",
redirect="https://findingfakeurlsisprettyhard.tv/oauth2", bot_token="bot-token-only-required-for-guild-joining-or-updating-linked-roles-metadata")
app = Flask(__name__)

client.update_linked_roles_metadata([
    {
        "type": 2,
        "key": "level",
        "name": "Level",
        "description": "The level the user is on"
    },
    {
        "type": 7,
        "key": "supporter",
        "name": "Supporter",
        "description": "Spent money to help the game"
    }
])

@app.route("/oauth2")
def oauth2():
    code = request.args.get("code")

    access = client.exchange_code(code)

    access.update_metadata("Platform Name", "Username",  level=69, supporter=True)

    identify = access.fetch_identify()
    connections = access.fetch_connections()
    guilds = access.fetch_guilds()

    return f"""{identify}<br><br>{connections}<br><br>{guilds}"""

app.run("0.0.0.0", 8080)
```

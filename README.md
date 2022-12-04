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
Don't forget to replace all the client information on line 20 and 21 with your application's own information. You can leave bot token empty if your not adding members to guilds.
```py
import discordoauth2
from flask import Flask, request

client = discordoauth2.Client(849930878276993044, secret="very-secret-code",
redirect="https://findingfakeurlsisprettyhard.tv/oauth2", bot_token="bot-token-only-required-for-guild-joining")
app = Flask(__name__)

@app.route("/oauth2")
def oauth2():
    code = request.args.get("code")

    access = client.exchange_code(code)

    identify = access.fetch_identify()
    connections = access.fetch_connections()
    guilds = access.fetch_guilds()

    return f"""{identify}<br><br>{connections}<br><br>{guilds}"""

app.run("0.0.0.0", 8080)
```

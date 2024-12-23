from flask import Flask, request, redirect
import discordoauth2

client = discordoauth2.Client(
    849930878276993044,
    "GPZugRwx_mscaZBqywF7V3_vq72SzaPk",
    "http://localhost:8080/oauth2",
)


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(client.generate_uri(["openid", "profile"]))


@app.route("/oauth2")
def oauth2():
    code = request.args.get("code")
    token = client.exchange_code(code)
    return token


app.run(port=8080)

import requests

class token_instance():
  def __init__(self, access_token, bot_token):
    self.token = access_token
    self.bot_token = bot_token
  
  def identify(self):
    headers = {
      'Authorization': f'Bearer {self.token}'
    }
    user_object = requests.get(url="https://discordapp.com/api/v9/users/@me",headers=headers)
    if user_object.status_code == 401: raise Exception(f"Scope wasn't granted in OAuth2.")
    if user_object.status_code == 429: raise Exception(f"You are being Rate Limited. Retry after: {user_object.json()['retry_after']}")
    return user_object.json()

  def connections(self):
    headers = {
      'Authorization': f'Bearer {self.token}'
    }
    user_object = requests.get(url="https://discordapp.com/api/v9/users/@me/connections",headers=headers)
    if user_object.status_code == 401: raise Exception(f"Scope wasn't granted in OAuth2.")
    if user_object.status_code == 429: raise Exception(f"You are being Rate Limited. Retry after: {user_object.json()['retry_after']}")
    return user_object.json()

  def guilds(self):
    headers = {
        'Authorization': f'Bearer {self.token}'
      }
    user_object = requests.get(url="https://discordapp.com/api/v9/users/@me/guilds",headers=headers)
    if user_object.status_code == 401: raise Exception(f"Scope wasn't granted in OAuth2.")
    if user_object.status_code == 429: raise Exception(f"You are being Rate Limited. Retry after: {user_object.json()['retry_after']}")
    return user_object.json()

  def guilds_member(self, guild):
    headers = {
        'Authorization': f'Bearer {self.token}'
      }
    user_object = requests.get(url=f"https://discordapp.com/api/v9/users/@me/guilds/{guild}/member",headers=headers)
    if user_object.status_code == 401: raise Exception(f"Scope wasn't granted in OAuth2.")
    if user_object.status_code == 429: raise Exception(f"You are being Rate Limited. Retry after: {user_object.json()['retry_after']}")
    return user_object.json()
  
  def guilds_join(self, guild):
    try:
      headers = {
        'Authorization': f'Bot {self.bot_token}',
        'Content-Type': 'application/json'
      }
      data = {
        'access_token': self.token
      }
      user_object = requests.put(url=f"https://discordapp.com/api/v9/guilds/{guild}/members/{self.identify()['id']}", json=data, headers=headers)
      if user_object.status_code == 401: raise Exception(f"Scope wasn't granted in OAuth2.")
      if user_object.status_code == 429: raise Exception(f"You are being Rate Limited. Retry after: {user_object.json()['retry_after']}")
      if user_object.status_code == 403: raise Exception(f"Provided token cannot invite people on Guild: {guild}. Guild ID may be incorrect.")
      return user_object
    except(requests.exceptions.HTTPError) as error:
      return error

class access_token():
  def __init__(self, response, token):
    self.access = token_instance(response["access_token"], token)
    self.expires = response["expires_in"]
    self.refresh_token = response["refresh_token"]
    
    try: self.webhook = response["webhook"]
    except(KeyError): self.webhook = None
    try: self.guild = response["guild"]
    except(KeyError): self.guild = None

class discordOauth2():
  def __init__(self, client, secret, redirect, token=None):
    self.client = client
    self.secret = secret
    self.redirect = redirect
    self.token = token
  
  def exchange_code(self, token):
    response = requests.post("https://discord.com/api/v9/oauth2/token", data={
      'client_id': self.client,
      'client_secret': self.secret,
      'grant_type': 'authorization_code',
      'code': token,
      'redirect_uri': self.redirect
    })
    if response.status_code == 429: raise Exception(f"You are being Rate Limited")
    elif response.status_code != 200: raise Exception(f"Something went wrong. Status Code: {response.status_code}")
    return access_token(response.json(), self.token)
  
  def refresh_token(self, refresh_token):
    response = requests.post("https://discord.com/api/v9/oauth2/token", data={
      'client_id': self.client,
      'client_secret': self.secret,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token
    })
    if response.status_code == 429: raise Exception(f"You are being Rate Limited")
    elif response.status_code != 200: raise Exception(f"Something went wrong. Status Code: {response.status_code}")
    return access_token(response.json(), self.token)

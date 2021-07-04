import requests

class token_instance():
  def __init__(self, access_token, bot_token):
    self.token = access_token
    self.bot_token = bot_token
  
  def identify(self):
    try:
      headers = {
       'Authorization': f'Bearer {self.token}'
      }
      user_object = requests.get(url="https://discordapp.com/api/users/@me",headers=headers)
      return user_object.json()
    except(requests.exceptions.HTTPError) as error:
      return error

  def connections(self):
    try:
      headers = {
        'Authorization': f'Bearer {self.token}'
      }
      user_object = requests.get(url="https://discordapp.com/api/users/@me/connections",headers=headers)
      return user_object.json()
    except(requests.exceptions.HTTPError) as error:
      return error

  def guilds(self):
    try:
      headers = {
          'Authorization': f'Bearer {self.token}'
        }
      user_object = requests.get(url="https://discordapp.com/api/users/@me/guilds",headers=headers)
      return user_object.json()
    except(requests.exceptions.HTTPError) as error:
      return error

  def join_guild(self, guild):
    try:
      headers = {
        'Authorization': f'Bot {self.bot_token}',
        'Content-Type': 'application/json'
      }
      data = {
        'access_token': self.token
      }
      user_object = requests.put(url=f"https://discordapp.com/api/guilds/{guild}/members/{self.identify}", json=data, headers=headers)
      return user_object.text
    except(requests.exceptions.HTTPError) as error:
      return error

class discordOauth2():
  endpoint = 'https://discord.com/api/v8'
  def __init__(self, client, secret, redirect, token=None):
    self.client = client
    self.secret = secret
    self.redirect = redirect
    self.token = token
  
  def exchange_code(self, token):
    data = {
      'client_id': self.client,
      'client_secret': self.secret,
      'grant_type': 'authorization_code',
      'code': token,
      'redirect_uri': self.redirect
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = requests.post(discordOauth2.endpoint+'/oauth2/token', data=data, headers=headers).json()
    return token_instance(data['access_token'], self.token)

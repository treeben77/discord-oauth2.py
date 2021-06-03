import requests

client = dict()

def client(payload):
  global client
  client = {
  'id': str(payload['client_id']),
  'secret': payload['client_secret'],
  'redirect_uri': payload['redirect_uri'],
  'token': payload['bot_token']
}
endpoint = 'https://discord.com/api/v8'

def exchange_code(token):
  data = {
    'client_id': client['id'],
    'client_secret': client['secret'],
    'grant_type': 'authorization_code',
    'code': token,
    'redirect_uri': client['redirect_uri']
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  return requests.post(endpoint+'/oauth2/token', data=data, headers=headers).json()

def refresh_token(token):
  data = {
    'client_id': client['id'],
    'client_secret': client['secret'],
    'grant_type': 'authorization_code',
    'code': token
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post(endpoint+'/oauth2/token', data=data, headers=headers)
  return r.json()

def get_identify(access_token):
  try:
    headers = {
      'Authorization': f'Bearer {access_token}'
    }
    user_object = requests.get(url="https://discordapp.com/api/users/@me",headers=headers)
    return user_object.json()
  except(requests.exceptions.HTTPError) as error:
    return error

def get_connections(access_token):
  try:
    headers = {
      'Authorization': f'Bearer {access_token}'
    }
    user_object = requests.get(url="https://discordapp.com/api/users/@me/connections",headers=headers)
    return user_object.json()
  except(requests.exceptions.HTTPError) as error:
    return error

def get_guilds(access_token):
  try:
    headers = {
      'Authorization': f'Bearer {access_token}'
    }
    user_object = requests.get(url="https://discordapp.com/api/users/@me/guilds",headers=headers)
    return user_object.json()
  except(requests.exceptions.HTTPError) as error:
    return error

def join_guild(access_token, guild):
  try:
    headers = {
      'Authorization': f'Bot {client["token"]}',
      'Content-Type': 'application/json'
    }
    data = {
      'access_token': access_token
    }
    user_object = requests.put(url=f"https://discordapp.com/api/guilds/{guild}/members/{get_identify(access_token)['id']}", json=data, headers=headers)
    return user_object.text
  except(requests.exceptions.HTTPError) as error:
    return error

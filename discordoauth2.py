import requests

# class User():
#   def __init__(self, data: dict):
#     self.id = int(data["id"])
#     self.username = data["username"]
#     self.avatar = data.get("avatar")
#     self.discriminator = data["discriminator"]
#     self.public_flags = data.get("public_flags")
#     self.flags = data.get("flags")
#     self.banner = data.get("banner")
#     self.accent_color = data.get("accent_color")
#     self.locale = data.get("locale")
#     self.mfa_enabled = data.get("mfa_enabled")
#     self.nitro_type = data.get("premium_type")
#     self.email = data.get("email")
#     self.email_verified = data.get("verified")
  
#   @property
#   def avatar_url(self):
#     if not self.avatar: return None
#     return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.{'png' if not self.avatar.startswith('a_') else '.gif'}?size=1024" 

#   @property
#   def banner_url(self):
#     if not self.banner: return None
#     return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.{'png' if not self.avatar.startswith('a_') else '.gif'}?size=1024" 

class access_token():
  def __init__(self, response, client):
    self.client = client
    self.expires = response["expires_in"]
    self.token = response["access_token"]
    self.scope = response["scope"].split(" ")
    self.refresh_token = response["refresh_token"]
    
    self.webhook = response.get("webhook")
    self.guild = response.get("guild")

    self.__identify_cache = None
  
  def identify(self):
    if not "identify" in self.scope: raise exceptions.MissingScope(f"identify scope wasn't granted")
    response = requests.get(url="https://discord.com/api/v10/users/@me",headers={
      'Authorization': f'Bearer {self.token}'
    })

    if response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}")
    elif not response.ok: raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    user =  response.json()
    self.__identify_cache = user
    return user

  def connections(self):
    if not "connections" in self.scope: raise exceptions.MissingScope(f"connections scope wasn't granted")
    response = requests.get(url="https://discord.com/api/v10/users/@me/connections", headers={
      'Authorization': f'Bearer {self.token}'
    })

    if response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}")
    elif not response.ok: raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    return response.json()

  def guilds(self):
    if not "guilds" in self.scope: raise exceptions.MissingScope(f"guilds scope wasn't granted")
    response = requests.get(url="https://discord.com/api/v10/users/@me/guilds",headers={
        'Authorization': f'Bearer {self.token}'
      })
    if response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}")
    elif not response.ok: raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    return response.json()

  def guilds_member(self, guild):
    if not "guilds.members.read" in self.scope: raise exceptions.MissingScope(f"guilds.members.read scope wasn't granted")
    response = requests.get(url=f"https://discord.com/api/v10/users/@me/guilds/{guild}/member",headers={
        'Authorization': f'Bearer {self.token}'
      })
    if response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}")
    elif not response.ok: raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    return response.json()
  
  def guilds_join(self, guild):
    if not self.__identify_cache: raise exceptions.BaseException(f"you must call identify before guilds.join!") 
    if not "guilds.join" in self.scope: raise exceptions.MissingScope(f"guilds.join scope wasn't granted")
    response = requests.put(url=f"https://discord.com/api/v10/guilds/{guild}/members/{self.__identify_cache['id']}", json={
      'Authorization': f'Bot {self.client.bot_token}',
    }, headers={
      'access_token': self.token
    })

    if response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}")
    elif not response.ok: raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    return response.json()

class Client():
  def __init__(self, id, secret, redirect, bot_token=None):
    self.id = id
    self.secret = secret
    self.redirect = redirect
    self.bot_token = bot_token
  
  def exchange_code(self, token):
    response = requests.post("https://discord.com/api/v10/oauth2/token", data={
      'client_id': self.id,
      'client_secret': self.secret,
      'grant_type': 'authorization_code',
      'code': token,
      'redirect_uri': self.redirect
    })

    if response.status_code == 429: raise Exception(f"You are being Rate Limited")
    elif response.status_code != 200: raise Exception(f"Something went wrong. Status Code: {response.status_code}")
    return access_token(response.json(), self)
  
  def refresh_token(self, refresh_token):
    response = requests.post("https://discord.com/api/v10/oauth2/token", data={
      'client_id': self.id,
      'client_secret': self.secret,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token
    })
    
    if response.status_code == 429: raise Exception(f"You are being Rate Limited")
    elif response.status_code != 200: raise Exception(f"Something went wrong. Status Code: {response.status_code}")
    return access_token(response.json(), self)
  
class exceptions():
  class BaseException(Exception):
    pass

  class HTTPException(BaseException):
    pass

  class RateLimited(HTTPException):
    def __init__(self, text, retry_after):
      self.retry_after = retry_after
      super().__init__(text)
  
  class Forbidden(HTTPException):
    pass

  class MissingScope(BaseException):
    pass

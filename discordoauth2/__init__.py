import requests
from datetime import datetime

class PartialAccessToken():
    def __init__(self, access_token, client) -> None:
        self.client = client
        self.token = access_token

    def revoke(self):
        return self.client.revoke_token(self.token, token_type="access_token")
    
    def fetch_identify(self):
        response = requests.get("https://discord.com/api/v10/users/@me", headers={
            "authorization": f"Bearer {self.token}"
        })

        if response.ok:
            return response.json()
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def fetch_connections(self):
        response = requests.get("https://discord.com/api/v10/users/@me/connections", headers={
            "authorization": f"Bearer {self.token}"
        })

        if response.ok:
            return response.json()
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def fetch_guilds(self):
        response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers={
            "authorization": f"Bearer {self.token}"
        })

        if response.ok:
            return response.json()
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def fetch_guild_member(self, guild_id):
        response = requests.get(f"https://discord.com/api/v10/users/@me/guilds/{guild_id}/member", headers={
            "authorization": f"Bearer {self.token}"
        })

        if response.ok:
            return response.json()
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 404: raise exceptions.HTTPException(f"user is not in this guild.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def join_guild(self, guild_id, user_id, nick = None, role_ids = None, mute = False, deaf = False):
        response = requests.put(f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}", headers={
            "authorization": f"Bot {self.client._Client__bot_token}"
        }, json={
            "access_token": self.token,
            "nick": nick,
            "roles": role_ids,
            "mute": mute,
            "deaf": deaf,
        })

        if response.status_code == 204:
            raise exceptions.HTTPException(f"member is already in the guild.")
        elif response.ok:
            return response.json()
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 403: raise exceptions.Forbidden(f"the Bot token must be for a bot in the guild that has permissions to create invites in the target guild and must have any other required permissions.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def update_metadata(self, platform_name=None, username=None, **metadata):
        def metadataTypeHook(item):
            if type(item) == bool:
                return 1 if item else 0
            if type(item) == datetime:
                return item.isoformat()
            else: return item
        response = requests.put(f"https://discord.com/api/v10/users/@me/applications/{self.client.id}/role-connection", headers={
            "authorization": f"Bearer {self.token}"}, json={
                "platform_name": platform_name,
                "platform_username": username,
                "metadata": {key: metadataTypeHook(value) for key, value in metadata.items()}
            })

        if response.ok:
            return response.json()
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")

class AccessToken(PartialAccessToken):
    def __init__(self, data, client) -> None:
        super().__init__(data["access_token"], client)

        self.expires = data.get("expires_in")
        self.scope = data.get("scope", "").split(" ")
        self.refresh_token = data.get("refresh_token")
        self.webhook = data.get("webhook")
        self.guild = data.get("guild")
    
    def revoke_refresh_token(self):
        return self.client.revoke_token(self.refresh_token, token_type="refresh_token")

class Client():
    def __init__(self, id, secret, redirect, bot_token=None):
        self.id = id
        self.redirect_url = redirect
        self.__secret = secret
        self.__bot_token = bot_token

    def update_linked_roles_metadata(self, metadata):
        requests.put(f"https://discord.com/api/v10/applications/{self.id}/role-connections/metadata", headers={
            "authorization": f"Bot {self.__bot_token}"}, json=metadata)
    
    def from_access_token(self, access_token):
        return PartialAccessToken(access_token, self)
    
    def exchange_code(self, code):
        response = requests.post("https://discord.com/api/v10/oauth2/token", data={
            "grant_type": "authorization_code", "code": code,
            "client_id": self.id, "client_secret": self.__secret,
            "redirect_uri": self.redirect_url})

        if response.ok:
            return AccessToken(response.json(), self)
        elif response.status_code == 400: raise exceptions.HTTPException("the code, client id, client secret or the redirect uri is invalid/don't match.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")    

    def refresh_token(self, refresh_token):
        response = requests.post("https://discord.com/api/v10/oauth2/token", data={
            "grant_type": "refresh_token", "refresh_token": refresh_token,
            "client_id": self.id, "client_secret": self.__secret})
        
        if response.ok:
            return AccessToken(response.json(), self)
        elif response.status_code == 400: raise exceptions.HTTPException("the refresh token, client id or client secret is invalid/don't match.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def client_credentails_grant(self, scope):
        response = requests.post("https://discord.com/api/v10/oauth2/token", data={
            "grant_type": "client_credentials", "scope": " ".join(scope)},
            auth=(self.id, self.__secret))
        if response.ok:
            return AccessToken(response.json(), self)
        elif response.status_code == 400: raise exceptions.HTTPException("the scope, client id or client secret is invalid/don't match.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")
    
    def revoke_token(self, token, token_type=None):
        response = requests.post("https://discord.com/api/oauth2/token/revoke",
            data={"token": token, "token_type_hint": token_type},
            auth=(self.id, self.__secret))
        print(response.status_code, response.text)
        if response.ok:
            return
        elif response.status_code == 401: raise exceptions.Forbidden(f"this AccessToken does not have the nessasary scope.")
        elif response.status_code == 429: raise exceptions.RateLimited(f"You are being Rate Limited. Retry after: {response.json()['retry_after']}", retry_after=response.json()['retry_after'])
        else:
            raise exceptions.HTTPException(f"Unexpected HTTP {response.status_code}")

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

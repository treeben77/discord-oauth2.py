import requests

from datetime import datetime
from typing import Optional, Union, Literal
from urllib import parse

from .exceptions import Exceptions


class PartialAccessToken:
    def __init__(self, access_token, client) -> None:
        self.client: Client = client
        self.token: str = access_token

    def revoke(self):
        """Shorthand for `Client.revoke_token` with the `PartialAccessToken`'s access token."""
        return self.client.revoke_token(self.token, token_type="access_token")

    def fetch_identify(self) -> dict:
        """Retrieves the user's [user object](https://discord.com/developers/docs/resources/user#user-object). Requires the `identify` scope and the `email` scope for their email address"""
        response = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"authorization": f"Bearer {self.token}"},
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def fetch_connections(self) -> list[dict]:
        """Retrieves a list of [connection object](https://discord.com/developers/docs/resources/user#connection-object)s the user has linked. Requires the `connections` scope"""
        response = requests.get(
            "https://discord.com/api/v10/users/@me/connections",
            headers={"authorization": f"Bearer {self.token}"},
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def fetch_guilds(self) -> list[dict]:
        """Retrieves a list of [partial guild](https://discord.com/developers/docs/resources/user#get-current-user-guilds-example-partial-guild)s the user is in. Requires the `guilds` scope"""

        response = requests.get(
            "https://discord.com/api/v10/users/@me/guilds",
            headers={"authorization": f"Bearer {self.token}"},
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def fetch_guild_member(self, guild_id: int) -> dict:
        """Retrieves the user's [guild member object](https://discord.com/developers/docs/resources/guild#guild-member-object) in a specific guild. Requires the `guilds.members.read` scope

        guild_id: The guild ID to fetch member info for
        """
        response = requests.get(
            f"https://discord.com/api/v10/users/@me/guilds/{guild_id}/member",
            headers={"authorization": f"Bearer {self.token}"},
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 404:
            raise Exceptions.HTTPException(f"user is not in this guild.")
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def join_guild(
        self,
        guild_id: int,
        user_id: int,
        nick: str = None,
        role_ids: list[int] = None,
        mute: bool = False,
        deaf: bool = False,
    ) -> dict:
        """Adds the user to a guild. Requires the `guilds.join` scope and `Client` must have a bot token, and the bot must have `CREATE_INSTANT_INVITE` in the guild it wants to add the member to. Returns a [guild member object](https://discord.com/developers/docs/resources/guild#guild-member-object)

        guild_id: The guild ID to add the user to
        user_id: The ID of the user. Retrievable with `PartialAccessToken.fetch_identify()['id']`
        nick: The nickname to give the user upon joining. Bot must also have `MANAGE_NICKNAMES`
        role_ids: A list of role IDs to give the user upon joining (bypasses Membership Screening). Bot must also have `MANAGE_ROLES`
        mute: Wether the user is muted in voice channels upon joining. Bot must also have `MUTE_MEMBERS`
        deaf: Wether the user is deaf in voice channels upon joining. Bot must also have `DEAFEN_MEMBERS`
        """
        response = requests.put(
            f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}",
            headers={"authorization": f"Bot {self.client._Client__bot_token}"},
            json={
                "access_token": self.token,
                "nick": nick,
                "roles": role_ids,
                "mute": mute,
                "deaf": deaf,
            },
        )

        if response.status_code == 204:
            raise Exceptions.HTTPException(f"member is already in the guild.")
        elif response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 403:
            raise Exceptions.Forbidden(
                f"the Bot token must be for a bot in the guild that has permissions to create invites in the target guild and must have any other required permissions."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def fetch_metadata(self):
        """Retrieves the user's [metadata](https://discord.com/developers/docs/resources/user#application-role-connection-object) for this application. Requires the `role_connections.write` scope"""
        response = requests.get(
            f"https://discord.com/api/v10/users/@me/applications/{self.client.id}/role-connection",
            headers={"authorization": f"Bearer {self.token}"},
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def update_metadata(
        self, platform_name: str = None, username: str = None, **metadata
    ) -> list[dict]:
        """Updates the user's metadata for this application. Requires the `role_connections.write` scope

        platform_name: the platform's name. Appears in full capitals at the top of the application box in the client.
        username: the user's name on the platform. Appears below the platform name,
        metadata: key and value pairs for metadata. Allows `bool`, `int`, `datetime`, and `str` (only iso timestamps) values.
        """

        def metadataTypeHook(item):
            if type(item) == bool:
                return 1 if item else 0
            if type(item) == datetime:
                return item.isoformat()
            else:
                return item

        response = requests.put(
            f"https://discord.com/api/v10/users/@me/applications/{self.client.id}/role-connection",
            headers={"authorization": f"Bearer {self.token}"},
            json={
                "platform_name": platform_name,
                "platform_username": username,
                "metadata": {
                    key: metadataTypeHook(value)
                    for key, value in metadata.items()
                },
            },
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def clear_metadata(self):
        """Clears the user's metadata for this application. Requires the `role_connections.write` scope"""
        response = requests.put(
            f"https://discord.com/api/v10/users/@me/applications/{self.client.id}/role-connection",
            headers={"authorization": f"Bearer {self.token}"},
            json={},
        )

        if response.ok:
            return response.json()
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )


class AccessToken(PartialAccessToken):
    def __init__(self, data, client) -> None:
        super().__init__(data["access_token"], client)

        self.id_token: Optional[str] = data.get("id_token")
        self.expires: int = data.get("expires_in")
        self.scope: list[str] = data.get("scope", "").split(" ")
        self.refresh_token: str = data.get("refresh_token")
        self.webhook: Optional[dict] = data.get("webhook")
        self.guild: Optional[dict] = data.get("guild")

    def revoke_refresh_token(self):
        """Shorthand for `Client.revoke_token` with the `AccessToken`'s refresh token."""
        return self.client.revoke_token(
            self.refresh_token, token_type="refresh_token"
        )


class Client:
    def __init__(
        self, id: int, secret: str, redirect: str, bot_token: str = None
    ):
        """Represents a Discord Application. Create an application on the [Developer Portal](https://discord.com/developers/applications)

        id: The application's ID
        secret: The application's Client Secret
        redirect: The redirect URL for OAuth2
        bot_token: The token for the application's bot. Only required for joining guilds and updating linked roles metadata.
        """
        self.id: int = id
        self.redirect_url: str = redirect
        self.__secret = secret
        self.__bot_token = bot_token

    def update_linked_roles_metadata(self, metadata: list[dict]):
        """Updates the application's linked roles metadata.

        metadata: List of [application role connection metadata](https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object)
        """
        requests.put(
            f"https://discord.com/api/v10/applications/{self.id}/role-connections/metadata",
            headers={"authorization": f"Bot {self.__bot_token}"},
            json=metadata,
        )

    def from_access_token(self, access_token: str) -> PartialAccessToken:
        """Creates a `PartialAccessToken` from an access token string.

        access_token: access token from `PartialAccessToken.token`
        """
        return PartialAccessToken(access_token, self)

    def exchange_code(self, code: str) -> AccessToken:
        """Converts a code from the redirect url into a `AccessToken`

        code: `code` parameter from OAuth2 redirect URL
        """
        response = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.id,
                "client_secret": self.__secret,
                "redirect_uri": self.redirect_url,
            },
        )

        if response.ok:
            return AccessToken(response.json(), self)
        elif response.status_code == 400:
            raise Exceptions.HTTPException(
                "the code, client id, client secret or the redirect uri is invalid/don't match."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def refresh_token(self, refresh_token: str) -> AccessToken:
        """Converts a refresh token into a new `AccessToken`

        refresh_token: refresh token from `AccessToken.refresh_token`
        """
        response = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.id,
                "client_secret": self.__secret,
            },
        )

        if response.ok:
            return AccessToken(response.json(), self)
        elif response.status_code == 400:
            raise Exceptions.HTTPException(
                "the refresh token, client id or client secret is invalid/don't match."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def client_credentails_grant(self, scope: list[str] = None) -> AccessToken:
        """Creates an `AccessToken` on behalf of the application. If the owner is a team, then only `identify` and `applications.commands.update` are allowed.

        *Identical to `client_credentials_grant` but with a typo for backwards compatibility.*

        scope: list of string scopes to authorize.
        """

        return self.client_credentials_grant(scope)

    def client_credentials_grant(self, scope: list[str]) -> AccessToken:
        """Creates an `AccessToken` on behalf of the application's owner. If the owner is a team, then only `identify` and `applications.commands.update` are allowed.

        scope: list of string scopes to authorize.
        """
        response = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "scope": " ".join(scope),
            },
            auth=(self.id, self.__secret),
        )
        if response.ok:
            return AccessToken(response.json(), self)
        elif response.status_code == 400:
            raise Exceptions.HTTPException(
                "the scope, client id or client secret is invalid/don't match."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def revoke_token(self, token: str, token_type: str = None):
        """Revokes a OAuth2 token related to the client.

        token: the token string to be revoked.
        token_type: the type of token to be revoked. This may be ignored by Discord.
        """
        response = requests.post(
            "https://discord.com/api/oauth2/token/revoke",
            data={"token": token, "token_type_hint": token_type},
            auth=(self.id, self.__secret),
        )
        print(response.status_code, response.text)
        if response.ok:
            return
        elif response.status_code == 401:
            raise Exceptions.Forbidden(
                f"this AccessToken does not have the necessary scope."
            )
        elif response.status_code == 429:
            raise Exceptions.RateLimited(
                f"You are being Rate Limited. Retry after: {response.json()['retry_after']}",
                retry_after=response.json()["retry_after"],
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected HTTP {response.status_code}"
            )

    def generate_uri(
        self,
        scope: Union[str, list[str]],
        state: Optional[str] = None,
        skip_prompt: Optional[bool] = False,
        integration_type: Optional[Literal["guild", "user"]] = "user",
        response_type: Optional[Literal["code", "token"]] = "code",
        guild_id: Optional[Union[int, str]] = None,
        disable_guild_select: Optional[bool] = None,
        permissions: Optional[Union[int, str]] = None,
    ) -> str:
        """Creates an authorization uri with client information prefilled.

        scope: a string, or list of strings for the scope
        state: optional state parameter. Optional but recommended.
        skip_prompt: doesn't require the end user to reauthorize if they've already authorized you app before. Defaults to `False`.
        response_type: either code, or token. token means the server can't access it, but the client can use it without converting.
        guild_id: the guild ID to add a bot/webhook.
        disable_guild_select: wether to allow the authorizing user to change the selected guild
        permissions: the permission bitwise integer for the bot being added.
        """
        params = {
            "client_id": self.id,
            "scope": " ".join(scope) if type(scope) == list else scope,
            "state": state,
            "redirect_uri": self.redirect_url,
            "prompt": "none" if skip_prompt else None,
            "response_type": response_type,
            "guild_id": guild_id,
            "disable_guild_select": disable_guild_select,
            "permissions": permissions,
        }
        if "applications.commands" in scope:
            params["integration_type"] = (
                0 if integration_type == "guild" else 1
            )
        return f"https://discord.com/oauth2/authorize?{parse.urlencode({key: value for key, value in params.items() if value is not None})}"

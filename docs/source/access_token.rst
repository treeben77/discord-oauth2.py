AccessToken
=============================

.. currentmodule:: discord-oauth2.py

.. class:: AccessToken()

   .. attribute:: client 

      The client which generated this AccessToken

      :type: :class:`discordoauth2.Client`
   
   .. atribute:: token

      The raw token for this AccessToken, you can use :class:`discordoauth2.Client.from_access_token` to use it again.

      :type: str
   
   .. atribute:: expires

      The number of seconds until it expires from when the instance was created.

      :type: int
   
   .. atribute:: scope

      A list of scopes that are provided.

      :type: list[str]
   
   .. atribute:: refresh_token

      The refresh_token for this AccessToken, you can use :class:`discordoauth2.Client.refresh_token` to use this authorization again after it expires.

      :type: str
   
   .. atribute:: webhook

      A `parital webhook object <https://discord.com/developers/docs/resources/webhook#webhook-object-webhook-structure>`__ if they was a ``webhook.incoming`` scope.

      :type: dict
   
   .. atribute:: guild

      A `partial guild object <https://discord.com/developers/docs/resources/guild#guild-object-guild-structure>`__ if a bot was added to a guild.

      :type: dict
   
   .. method:: fetch_identify()

      Returns a dictionary with a `user object <https://discord.com/developers/docs/resources/user#user-object-user-structure>`__ which includes ``email`` and ``verified`` (verified email) if the ``email`` scope is provided
   
      :returns: :class:`dict`
      :raises discordoauth2.exceptions.HTTPException: The request failed
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the identify scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: fetch_connections()

      Returns a list of `connection objects <https://discord.com/developers/docs/resources/user#connection-object-connection-structure>`__
   
      :returns: :class:`list`
      :raises discordoauth2.exceptions.HTTPException: The request failed
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the connections scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   
   .. method:: fetch_guilds()

      Returns a list of partial `guild objects <https://discord.com/developers/docs/resources/guild#guild-object>`__
   
      :returns: :class:`list`
      :raises discordoauth2.exceptions.HTTPException: The request failed
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: fetch_guild_member(guild_id)

      Returns a partial `guild member object <https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-structure>`__
   
      :param int guild_id: The guild ID to retrieve member data from.

      :returns: :class:`dict`
      :raises discordoauth2.exceptions.HTTPException: The request failed, possibly because the member is not in the guild.
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.member.read scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.

   .. method:: join_guild(guild_id, nick = None, role_ids = None, mute = False, deaf = False)

      Adds the user to a guild. The application's bot must also be in the guild, have invite permissions and it's bot token must also be provided.
   
      :param int guild_id: The guild ID to retrieve member data from.
      :param str nick: The nickname the member should have when they join.
      :param list[int] role_ids: a List of role IDs to assign them when they join.
      :param bool mute: Wether they should be server muted when they join.
      :param bool deaf: Wether they should be server deafend when they join.
      
      :returns: :class:`dict`
      :raises discordoauth2.exceptions.HTTPException: The request failed
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.join scope or the bot isn't in the guild/have the correct permissions.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: fetch_metadata()

      Returns the user's `metadata object <https://discord.com/developers/docs/resources/user#application-role-connection-object>`__ for this application.
   
      .. versionadded:: 1.1

      :returns: :class:`dict`
      :raises discordoauth2.exceptions.HTTPException: The request failed, possibly because the member is not in the guild.
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.member.read scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: update_metadata(platform_name=None, username=None, **metadata)

      Updates and returns the user's `metadata object <https://discord.com/developers/docs/resources/user#application-role-connection-object>`__ for this application.
   
      .. versionadded:: 1.1

      :param str platform_name: Text that appears at the top of the app connection box, usally denoting the platform's name.
      :param str platform_username: Text that appears under the platform name, large, and usally denoting the user's name on the platform.
      :param dict metadata: List of keys and values to set the user's metadata. Supported types: :class:`bool`, :class:`datetime.datetime`, :class:`int`
            
      :returns: :class:`dict`
      :raises discordoauth2.exceptions.HTTPException: The request failed, possibly because the member is not in the guild.
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.member.read scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. warning::

      You must make sure to store the access token and refresh token, otherwise you won't be able to update or remove the metadata later.
   
   .. method:: clear_metadata()

      Removes the user's `metadata object <https://discord.com/developers/docs/resources/user#application-role-connection-object>`__ for this application.
   
      .. versionadded:: 1.1
      
      :returns: :class:`dict`
      :raises discordoauth2.exceptions.HTTPException: The request failed, possibly because the member is not in the guild.
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.member.read scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.

   .. method:: revoke()

      Shorthand for :meth:`Client.revoke_token`, it will revoke the access token and any related refresh token.
   
      .. versionadded:: 1.1
      
      :raises discordoauth2.exceptions.HTTPException: The request failed, possibly because the member is not in the guild.
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.member.read scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: revoke_refresh_token()

      Shorthand for :meth:`Client.revoke_token`, it will revoke the refresh token and any related access token.
   
      .. versionadded:: 1.1
      
      :raises discordoauth2.exceptions.HTTPException: The request failed, possibly because the member is not in the guild.
      :raises discordoauth2.exceptions.Forbidden: The AccessToken doesn't have the guilds.member.read scope.
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.

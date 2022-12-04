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

      The webhook URL if they was a webhook scope.

      :type: str
   
   .. atribute:: guild

      The guild ID if a bot was added to a guild.

      :type: int
   
   .. method:: fetch_identify()

      Returns a dictionary with a `user object <https://discord.com/developers/docs/resources/user#user-object-user-structure>`__ which includes email if the email scope is provided
   
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

      Returns a parial `guild member object <https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-structure>`__
   
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
   
.. class:: PartialAccessToken()

   .. attribute:: client 

      The client which generated this AccessToken

      :type: :class:`discordoauth2.Client`
   
   .. atribute:: token

      The raw token for this AccessToken, you can use :class:`discordoauth2.Client.from_access_token` to use it again.

      :type: str
   
   .. method:: fetch_identify()

      Returns a dictionary with a `user object <https://discord.com/developers/docs/resources/user#user-object-user-structure>`__ which includes email if the email scope is provided
   
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

      Returns a parial `guild member object <https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-structure>`__
   
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
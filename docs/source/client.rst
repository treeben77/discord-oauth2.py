Client
=============================

.. currentmodule:: discordoauth2

.. class:: Client(id, secret, redirect, bot_token=None)

   :param int id: The application ID
   :param str secret: The applications secret, this should be secret!
   :param str redirect: The redirect URL for oauth2
   :param str bot_token: When adding a user to a guild, a bot with sufficent permissions is required. if you're not going to add members to a guild leave this empty.

   .. attribute:: id 

      The application's ID

      :type: int
   
   .. attribute:: redirect_url

      The redirect URL 

      :type: str
   
   .. method:: from_access_token(access_token)

      Creates a :class:`discordoauth2.PartialAccessToken` object from a code. This is useful so you can store the :attr:`PartialAccessToken.token` and then continue using it.
   
      :param str access_token: The code from oauth2, it is the code paramater on successful return redirect urls from discord's oauth2.
      
      :returns: :class:`discordoauth2.PartialAccessToken`
   
   .. method:: exchange_code(code)

      Converts a code from the redirect url into a :class:`discordoauth2.AccessToken`
   
      :param str code: `code` paramater from OAuth2 redirect URL
      
      :returns: :class:`discordoauth2.AccessToken`
      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: refresh_token(refresh_token)

      Converts a refresh token into a new :class:`discordoauth2.AccessToken`. You should store the refresh token and access token, so you can renew the access token when it expires.
   
      :param str refresh_token: The refresh token, can be found from :attr:`discordoauth2.AccessToken.refresh_token`

      :returns: :class:`discordoauth2.AccessToken`
      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: client_credentails_grant(scope)

      Creates an :class:`discordoauth2.AccessToken` on behalf of the application's owner.
   
      :param list[str] scope: List of scopes.

      :returns: :class:`discordoauth2.AccessToken`
      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. warning::

      If the application is owned by a team, you can only request for the ``identify`` scope. You can also request ``applications.commands.update``, but the library does not support it yet.``
   
   .. method:: revoke_token(token, token_type=None)

      Revokes an OAuth2 token related to the client.
   
      .. versionadded:: 1.1
         
      :param str token: Access/Refresh token to revoke
      :param Optional[str] token_type: Not required, but should be either ``refresh_token`` or ``access_token``

      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: update_linked_roles_metadata(metadata)

      Updates the application's linked roles metadata, requires bot token to have been provided.

      .. versionadded:: 1.1

      :param dict metadata: Should be a list of `application role connection metadata <https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object>`__
   
   .. note::

      The bot token is required to update metadata.
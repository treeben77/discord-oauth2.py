Client
=============================

.. currentmodule:: discord-oauth2.py

.. class:: Client(id, secret, redirect, bot_token=None)

   :param int id: The application ID
   :param str secret: The applications secret, this should be secret!
   :param str redirect: The redirect URL for oauth2
   :param str bot_token: When adding a user to a guild, a bot with sufficent permissions is required. if you're not going to add members to a guild leave this empty.

   .. attribute:: id 

      The application ID

      :type: int
   
   .. atribute:: redirect_url

      The redirect URL 

      :type: str
   
   .. method:: from_access_token(access_token)

      Creates a PartialAccessToken object from a code. This is useful so you can store the :attr:`PartialAccessToken.token` and then continue using it.
   
      :param str access_token: The code from oauth2, it is the code paramater on successful return redirect urls from discord's oauth2.
      
      :returns: :class:`discordoauth2.PartialAccessToken`
   
   .. method:: exchange_code(code)

      Creates an AccessToken object from a code.
   
      :param str code: The code from oauth2, it is the code paramater on successful return redirect urls from discord's oauth2.
      
      :returns: :class:`discordoauth2.AccessToken`
      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: refresh_token(refresh_token)

      Creates an AccessToken object from a refresh_token. Refresh tokens are to refresh the access token when it expires.
   
      :param str refresh_token: The refresh token, can be found from :attr:`discordoauth2.AccessToken.refresh_token`

      :returns: :class:`discordoauth2.AccessToken`
      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.
   
   .. method:: client_credentails_grant(scope)

      Creates an AccessToken object for the application's owner with the provided scope.
   
      :param list[str] scope: The scope is strings divided by a list.

      :returns: :class:`discordoauth2.AccessToken`
      :raises discordoauth2.exceptions.HTTPException: The request failed, usally because the client ID, client, secret, redirect or code is incorrect
      :raises discordoauth2.exceptions.RateLimited: You're being rate limited.

   .. warning::

      If the application is owned by a team, you can only request for the `identify` scope. You can also request `applications.commands.update`, but the library does not support it yet.
         
   .. autofunction:: discordoauth2.revoke_token
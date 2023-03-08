Welcome to ``discordoauth2.py``!
===============

Table of Contents
----------

.. toctree::

   :maxdepth: 1

   client
   access_token

Quickstart
-------------------------------------------

Installing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install the library with pip using this command:

.. code::

   pip install discord-oauth2.py

Fetching User Data Flask Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Don't forget to replace all the client information below with your application's own information. You can leave bot token empty if your not adding members to guilds or updating linked roles metadata.

.. code::
   
   import discordoauth2
   from flask import Flask, request

   client = discordoauth2.Client(849930878276993044, secret="very-secret-code",
   redirect="https://findingfakeurlsisprettyhard.tv/oauth2", bot_token="bot-token-only-required-for-guild-joining")
   app = Flask(__name__)

   @app.route("/oauth2")
   def oauth2():
      code = request.args.get("code")

      access = client.exchange_code(code)

      identify = access.fetch_identify()
      connections = access.fetch_connections()
      guilds = access.fetch_guilds()

      return f"""{identify}<br><br>{connections}<br><br>{guilds}"""

   app.run("0.0.0.0", 8080)

Linked Roles Flask Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Don't forget to replace all the client information below with your application's own information.

.. code::
   
   import discordoauth2
   from flask import Flask, request
   from datetime import datetime

   client = discordoauth2.Client(849930878276993044, secret="very-secret-code",
   redirect="https://findingfakeurlsisprettyhard.tv/oauth2", bot_token="bot-token-only-required-for-guild-joining")

   client.update_linked_roles_metadata([
      {
         "type": 2,
         "key": "level",
         "name": "Level",
         "description": "The user's XP level."
      },
      {
         "type": 6,
         "key": "join",
         "name": "Joined",
         "description": "The date the user joined."
      },
      {
         "type": 7,
         "key": "supporter",
         "name": "Supporter",
         "description": "Wether the user has supported us."
      }
   ])

   app = Flask(__name__)

   @app.route("/oauth2")
   def oauth2():
      code = request.args.get("code")

      access = client.exchange_code(code)
      access.update_metadata("Example Game", username="TreeBen77", level=24, join=datetime.now(), supporter=True)

      return f"updated your metadata!"

   app.run("0.0.0.0", 8080)
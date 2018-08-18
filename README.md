# SplunkDiscord
Discord Webhook for Splunk Alerts

This is a drop in app for sending splunk alerts via webhook to a Discord channel. The built-in webhook needed to be modified in order for Discord to accept the request.

Most of the original splunk webhook was retained, modifications have been made to the stanza from webhook to alerts_discord in order to have a completely separate app from the built-in webhook app.

![Chat_Example](https://i.imgur.com/Camwykz.png?raw=true)

### /bin/
*alerts_discord.py*

This file is where the modifications took places, since Discord would not accept an entire payload by Splunk my solution was to load the json payload, extract the fields I wanted and insert those results into another payload which I then rencoded and sent in to Discord 



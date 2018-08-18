import sys
import json
import urllib2
import datetime

def send_discord_message(settings):


    #load Splunk Json, extract raw alert, source and time
    body = json.dumps(payload)
    resp = json.loads(body)
    source = resp['result']['source']
    time = resp['result']['_time']
    raw = resp['result']['_raw']
    resultslink = resp.get('results_link')
    alertname = resp.get('search_name')

    # converttime to human readable format
    human = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%Y-%m-%d %H:%M:%S')

    #Grab Configuration Settings
    user_agent = {"User-Agent": 'Splunk'}
    url = config.get('url')

    #the actual payload that goes to discord
    discordload = {
      "embeds": [
        {
          "title": "Search Results",
          "url": resultslink,
          "color": 16711680,
          "fields": [
            {
                "name": "Alert Name",
                "value": alertname,
            },
            {
                "name": "Raw Log",
                "value": raw,
            },
            {
                "name": "Source",
                "value": source,
            },
            {
                "name": "Time",
                "value": human
            }
          ]

        }
      ]
    }
    #Encodes the Discord Payload to be used with urllib
    body = json.dumps(discordload)

    print >> sys.stderr, 'DEBUG Calling url="%s" with body=%s' % (url, body)
    req = urllib2.Request(url, body, user_agent)
    try:
        res = urllib2.urlopen(req)
        body = res.read()
        print >> sys.stderr, "INFO discord API responded with HTTP status=%d" % res.code
        print >> sys.stderr, "DEBUG discord API response: %s" % json.dumps(body)
        return 200 <= res.code < 300
    except urllib2.HTTPError, e:
        print >> sys.stderr, "ERROR Error sending message: %s" % e
        print >> sys.stderr, json.dumps(body)
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        config = payload.get('configuration')
        if not send_discord_message(config):
            print >> sys.stderr, "FATAL Sending the discord message failed"
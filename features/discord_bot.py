import requests
import json
import glob
import sys, os
import datetime
from discord import Webhook, RequestsWebhookAdapter, File
from constants import DISCORD_WEBHOOK, ENVIRONMENT


baseURL = "https://discordapp.com/api/webhooks/{}".format(DISCORD_WEBHOOK)
webhook = Webhook.from_url(baseURL, adapter=RequestsWebhookAdapter())

path_to_report = os.path.join('reports', '*.html')
files = [File(open(path, 'rb'), os.path.basename(path)) for path in glob.glob(path_to_report)]

str_start = sys.argv[1]
str_finish = sys.argv[2]
str_diff = str(datetime.timedelta(seconds=int(sys.argv[3])))

message = f"""Test run results:\n
Started at {str_start}, finished at {str_finish} \n
Total duration: {str_diff} \n
Environment: {ENVIRONMENT}"""
webhook.send(message, username='TestResultsBot', files=files)
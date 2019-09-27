import requests
import json
import glob
import sys, os
import datetime
from discord import Webhook, RequestsWebhookAdapter, File
from constants import DISCORD_WEBHOOK, ENVIRONMENT, CONFIG_FILE

if DISCORD_WEBHOOK:
    baseURL = "https://discordapp.com/api/webhooks/{}".format(DISCORD_WEBHOOK)
    webhook = Webhook.from_url(baseURL, adapter=RequestsWebhookAdapter())

    str_start = sys.argv[1]
    str_finish = sys.argv[2]
    pattern = '%H:%M:%S'
    diff = datetime.datetime.strptime(str_finish, pattern) - datetime.datetime.strptime(str_start, pattern)
    str_diff = str(diff)

    str_start_replaced = str_start.replace(':', '_')
    path_to_report = os.path.join('reports', '*.html')
    files = [File(open(path, 'rb'), os.path.basename(path).replace('.', f'{ENVIRONMENT}_{CONFIG_FILE}_{str_start_replaced}.')) for path in glob.glob(path_to_report)]

    

    message = f"""
    ++++++++++++++++++++++++++++++++++++++++++++++
    Test run results:
    Started at {str_start}, finished at {str_finish}
    Total duration: {str_diff}
    Environment: {ENVIRONMENT}
    Config: {CONFIG_FILE}
    ===============================================
    """
    webhook.send(message, username='TestResultsBot', files=files)

import json
import os
from typing import Optional

from now_playing.functions import get_slack_post_instance, get_radio_station_instances


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    slack_api_token: Optional[str] = os.environ.get('SLACK_API_TOKEN')
    if slack_api_token is None:
        raise KeyError('Slack api token is not set')
    slack_post_now_playing = get_slack_post_instance(slack_api_token)
    radio_stations = get_radio_station_instances(event['radio_stations'])

    body = []
    for station in radio_stations:
        item = slack_post_now_playing.exec(station)
        body.append(item)
        print(json.dumps(item))

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

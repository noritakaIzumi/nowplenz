import json

from now_playing.functions import get_slack_post_instance, get_radio_station_instances


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    slack_post_now_playing = get_slack_post_instance(event['token']['secret_arn'], event['token']['region'])
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

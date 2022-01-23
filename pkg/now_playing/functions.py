from typing import List, Dict

from .core import AbstractRadioStation, SlackPostNowPlaying
from .radio_stations import RADIO_STATION_MAP


def get_slack_post_instance(token_secret_arn: str, token_region: str) -> SlackPostNowPlaying:
    return SlackPostNowPlaying(token_secret_arn=token_secret_arn, token_region=token_region)


def get_radio_station_instances(stations: List[Dict[str, str]]) -> List[AbstractRadioStation]:
    instances: list = []

    for station in stations:
        if station['station_key'] not in RADIO_STATION_MAP.keys():
            continue
        _class = RADIO_STATION_MAP[station['station_key']]
        instances.append(_class(
            slack_post_channel=station['slack_post_channel'],
            iam_username=station['tag_iam_username']
        ))

    return instances

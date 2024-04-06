from typing import List, TypedDict

from .core import AbstractRadioStation, SlackPostNowPlaying
from .radio_stations import RADIO_STATION_MAP


def get_slack_post_instance(slack_api_token: str) -> SlackPostNowPlaying:
    return SlackPostNowPlaying(slack_api_token=slack_api_token)

class Station(TypedDict):
    station_key: str
    slack_post_channel: str
    tag_iam_username: str

def get_radio_station_instances(stations: List[Station]) -> List[AbstractRadioStation]:
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

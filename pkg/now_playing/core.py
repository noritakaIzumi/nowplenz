import hashlib
import json
from abc import abstractmethod
from typing import Dict, final
from urllib import request, parse

import boto3

from metaclass_util import build_required_attributes_metaclass


@final
class SongInfo:
    """曲情報。オンエア曲リストで取得した情報からインスタンスを作成する。

    Attributes:
        song_name (str):
        artist_name (str):
        cd_image_url (str):

    """

    def __init__(
            self,
            song_name: str,
            artist_name: str,
            cd_image_url: str,
    ) -> None:
        self.song_name = song_name
        self.artist_name = artist_name
        self.cd_image_url = cd_image_url
        self.google_search_url = self.get_google_search_url()
        self.youtube_search_url = self.get_youtube_search_url()

    def get_google_search_url(self) -> str:
        return 'https://www.google.com/search?q=' \
               + parse.quote('%s %s' % (self.song_name, self.artist_name))

    def get_youtube_search_url(self) -> str:
        return 'https://www.youtube.com/results?search_query=' \
               + parse.quote('%s %s' % (self.song_name, self.artist_name))

    def get_hash(self) -> str:
        """曲名・アーティスト名からハッシュを生成する。

        Notes:
            オンエア曲リストが更新されたかどうか判定する際に用いる。

        """
        return hashlib.sha512((self.song_name + self.artist_name).encode()).hexdigest()


class AbstractRadioStation(metaclass=build_required_attributes_metaclass([
    {'name': 'tag_key', 'type': str},
])):
    """
    Attributes:
        station_name (str):
        station_url (str):
        np_url (str):
        icon_url (str):
        slack_post_channel (str): 投稿するチャンネル。
        iam_username (str): 曲情報ハッシュを格納する IAM ユーザ。
    """
    tag_key: str = ''
    """str: 曲情報ハッシュを格納する際のキー名。
    
    This param is required.
    """

    def __init__(self, slack_post_channel: str, iam_username: str) -> None:
        """

        Args:
            slack_post_channel (str):
            iam_username (str):
        """
        self.station_name = self.get_radio_station_name()
        self.station_url = self.get_station_url()
        self.np_url = self.get_np_url()
        self.icon_url = self.get_icon_url()
        self.slack_post_channel = slack_post_channel
        self.iam_username = iam_username

    @abstractmethod
    def get_radio_station_name(self) -> str:
        """ラジオ局名をセットします．

        Returns:
            str:

        """
        pass

    @abstractmethod
    def get_station_url(self) -> str:
        """ラジオ局 URL をセットします．

        Returns:
            str:

        """
        pass

    @abstractmethod
    def get_np_url(self) -> str:
        """Now Playing ページの URL をセットします．

        Examples:
            ラジオ局とドメインが同じ場合は ``self.station_url`` を利用してセットするといいでしょう::

                self.station_url + '/filepath'

            ラジオ局とドメインが異なる場合など，直接指定することもできます::

                'https://another.example.com/filepath'

        Returns:
            str:

        """
        pass

    def get_icon_url(self) -> str:
        """アイコン URL をセットします．

        Returns:
            str:

        Notes:
            このメソッドをオーバーライドしない場合は `favicon.ico` が指定されます．

        """
        return self.station_url + '/favicon.ico'

    @abstractmethod
    def get_song_info(self) -> SongInfo:
        """曲情報をセットします．``SongInfo`` のインスタンスを指定してください．

        Returns:
            SongInfo:

        """
        pass

    @final
    def song_is_latest(self, _hash: str) -> bool:
        """IAM ユーザのタグに格納されているハッシュと、取得した曲情報のハッシュを比較し、曲が最新かどうかを判定します。

        Args:
            _hash (str):

        Returns:
            曲が最新すなわちハッシュが一致するとき True を返します。

        """
        from mypy_boto3_iam import IAMClient
        client: IAMClient = boto3.client('iam')

        response = client.list_user_tags(UserName=self.iam_username)

        for tag in response['Tags']:
            if tag['Key'] == self.__class__.tag_key and tag['Value'] == _hash:
                return True

        client.tag_user(
            UserName=self.iam_username,
            Tags=[
                {
                    'Key': self.__class__.tag_key,
                    'Value': _hash,
                }
            ],
        )

        return False


@final
class SlackPostNowPlaying:
    def __init__(self, slack_api_token: str) -> None:
        self.token = slack_api_token

    def __post_to_slack(self, radio_station: AbstractRadioStation, song_info: SongInfo):
        station_name = radio_station.station_name
        icon_url = radio_station.icon_url
        slack_post_channel = radio_station.slack_post_channel
        np_url = radio_station.np_url

        payload = {
            "username": f'{station_name} Now Playing',
            "icon_url": icon_url,
            "channel": slack_post_channel,
            "text": f':radio: [{station_name}] {song_info.artist_name} - {song_info.song_name}',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'*{song_info.song_name}*\n{song_info.artist_name}'
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": song_info.cd_image_url,
                        "alt_text": "cd_image"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":mag: Search on Google",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "url": song_info.google_search_url
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":film_projector: Search on YouTube",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "url": song_info.youtube_search_url
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": f':guitar: Check {station_name}\'s on air music',
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "url": np_url,
                        }
                    ]
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer ' + self.token,
        }

        req = request.Request('https://slack.com/api/chat.postMessage', json.dumps(payload).encode(), headers)
        with request.urlopen(req) as res:
            status = res.read().decode('utf-8')

        return json.loads(status)

    def exec(self, radio_station: AbstractRadioStation) -> Dict:
        song_info = radio_station.get_song_info()
        _hash = song_info.get_hash()

        if radio_station.song_is_latest(_hash):
            return {
                'noa': {},
                'status': '',
            }

        status = self.__post_to_slack(radio_station, song_info)

        return {
            'noa': {
                'song': song_info.song_name,
                'artist': song_info.artist_name,
                'cd_image': song_info.cd_image_url,
                'google_search_url': song_info.google_search_url,
                'hash': _hash,
            },
            'status': status,
        }

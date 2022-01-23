import re
from abc import abstractmethod
from typing import IO
from urllib import request

from bs4 import BeautifulSoup

from now_playing.core import AbstractRadioStation, SongInfo


class MtmDefaultRadioStation(AbstractRadioStation):
    """全国 FM 連合デフォルト UI を使用しているラジオ局
    """

    tag_key = ''

    def __init__(self, *args, **kwargs):
        self.station_id = self.get_station_id()
        super().__init__(*args, **kwargs)

    @abstractmethod
    def get_radio_station_name(self) -> str:
        pass

    @abstractmethod
    def get_station_url(self) -> str:
        pass

    @abstractmethod
    def get_station_id(self) -> str:
        return ''

    def get_np_url(self) -> str:
        # noinspection HttpUrlsUsage
        return f'http://www.keitai.fm/search/view/{self.station_id}/'

    def get_song_info(self) -> SongInfo:
        f: IO
        with request.urlopen(self.np_url) as f:
            soup = BeautifulSoup(f.read().decode('utf-8'), 'html.parser')
            elements = soup.select('#searchResult .entry')

            element = BeautifulSoup(str(elements[0]), 'html.parser')
            song_name_obj = element.select('dd:nth-of-type(1) .entryTxt a')
            if not song_name_obj:
                song_name_obj = element.select('dd:nth-of-type(1) .entryTxt')
            song_name = song_name_obj[0].string.strip()
            artist = element.select('dd:nth-of-type(2)')[0].string
            search = re.search(r'https?://.*', element.select('dd:nth-of-type(1) .entryThum > img')[0]['src'])
            if search:
                cd_image_url = search.group()
            else:
                cd_image_url = f'{self.np_url}/img/noimage_35.gif'

        return SongInfo(song_name, artist, cd_image_url)

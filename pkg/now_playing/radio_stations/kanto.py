import re
from typing import IO
from urllib import request

from bs4 import BeautifulSoup

from now_playing.core import AbstractRadioStation, SongInfo


class JWaveRadioStation(AbstractRadioStation):
    """J-WAVE (東京)
    """
    tag_key = 'jwave'

    def get_radio_station_name(self) -> str:
        return 'J-WAVE'

    def get_station_url(self) -> str:
        return 'https://www.j-wave.co.jp'

    def get_np_url(self) -> str:
        return self.station_url + '/songlist'

    def get_song_info(self) -> SongInfo:
        f: IO
        with request.urlopen(self.np_url) as f:
            soup = BeautifulSoup(f.read().decode('utf-8'), 'html.parser')
            elements = soup.select('section#block_nowplaying .song')

            element = BeautifulSoup(str(elements[0]), 'html.parser')
            song_name = element.select('.song_info > h4')[0].string
            artist = element.select('.song_info > .txt_artist > span')[0].string
            search = re.search(r'(?<=url\()https?://.*(?=\))', element.select('.img > figure')[0]['style'])
            if search:
                cd_image_url = search.group()
            else:
                cd_image_url = f'{self.np_url}/images/jacket.jpg'

        return SongInfo(song_name, artist, cd_image_url)

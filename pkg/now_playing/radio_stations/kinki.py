from typing import IO
from urllib import request

from bs4 import BeautifulSoup

from now_playing.core import AbstractRadioStation, SongInfo
from now_playing.radio_stations import MtmDefaultRadioStation


class FmOsakaRadioStation(MtmDefaultRadioStation):
    """FM大阪
    """
    tag_key = 'fmosaka'

    def get_radio_station_name(self) -> str:
        return 'FM大阪'

    def get_station_url(self) -> str:
        return 'https://www.fmosaka.net/'

    def get_station_id(self) -> str:
        return 'bu'


class KissFmKobeRadioStation(MtmDefaultRadioStation):
    """Kiss FM KOBE
    """
    tag_key = 'kiss-fm'

    def get_radio_station_name(self) -> str:
        return 'Kiss FM KOBE'

    def get_station_url(self) -> str:
        return 'https://www.kiss-fm.co.jp/'

    def get_station_id(self) -> str:
        return 'iv'

    def get_icon_url(self) -> str:
        return self.station_url + '/assets/img/common/cmn_img_kisslogo_v.svg'


class Fm802RadioStation(AbstractRadioStation):
    """FM802 (大阪)
    """
    tag_key = 'fm802'

    def get_radio_station_name(self) -> str:
        return 'FM802'

    def get_station_url(self) -> str:
        return 'https://funky802.com'

    def get_np_url(self) -> str:
        return self.station_url + '/site/onairlist'

    def get_song_info(self) -> SongInfo:
        f: IO
        with request.urlopen(self.np_url) as f:
            soup = BeautifulSoup(f.read().decode('utf-8'), 'html.parser')
            elements = soup.select('div.c-infoOnair__lists > div:nth-child(1)')
            element_soup = BeautifulSoup(str(elements[0]), 'html.parser')
            song_name = element_soup.select('.c-infoOnair__list--title')[0].string
            artist = element_soup.select('.c-infoOnair__list--artist')[0].string
            cd_image_url = element_soup.select('.c-infoOnair__list--img > a > img')[0]['src']
            if cd_image_url[0] == '/':
                cd_image_url = self.station_url + cd_image_url

        return SongInfo(song_name, artist, cd_image_url)


class FmShigaRadioStation(MtmDefaultRadioStation):
    """FM 滋賀
    """
    tag_key = 'e-radio'

    def get_radio_station_name(self) -> str:
        return 'FM 滋賀'

    def get_station_url(self) -> str:
        return 'https://www.e-radio.co.jp/'

    def get_station_id(self) -> str:
        return 'uv'

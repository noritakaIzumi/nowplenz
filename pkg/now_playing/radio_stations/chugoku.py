"""中国地方
"""
from now_playing.radio_stations import MtmDefaultRadioStation


class FmSaninRadioStation(MtmDefaultRadioStation):
    """FM 山陰
    """
    tag_key = 'fm-sanin'

    def get_radio_station_name(self) -> str:
        return 'FM 山陰'

    def get_station_url(self) -> str:
        # noinspection HttpUrlsUsage
        return 'http://www.fm-sanin.co.jp/'

    def get_station_id(self) -> str:
        return 'vu'


class FmOkayamaRadioStation(MtmDefaultRadioStation):
    """FM OKAYAMA
    """
    tag_key = 'fm-okayama'

    def get_radio_station_name(self) -> str:
        return 'FM OKAYAMA'

    def get_station_url(self) -> str:
        # noinspection HttpUrlsUsage
        return 'http://www.fm-okayama.co.jp/'

    def get_station_id(self) -> str:
        return 'vv'


class HiroshimaFmRadioStation(MtmDefaultRadioStation):
    """広島 FM
    """
    tag_key = 'hiroshima-fm'

    def get_radio_station_name(self) -> str:
        return 'HFM'

    def get_station_url(self) -> str:
        # noinspection HttpUrlsUsage
        return 'http://www.hiroshima-fm.co.jp/'

    def get_station_id(self) -> str:
        return 'gu'


class FmYamaguchiRadioStation(MtmDefaultRadioStation):
    """FM 山口
    """
    tag_key = 'fmy'

    def get_radio_station_name(self) -> str:
        return 'FMY'

    def get_station_url(self) -> str:
        return 'https://www.fmy.co.jp/'

    def get_station_id(self) -> str:
        return 'uu'

from now_playing.radio_stations import MtmDefaultRadioStation


class FmAkitaRadioStation(MtmDefaultRadioStation):
    """エフエム秋田
    """
    tag_key: str = 'fm-akita'

    def get_radio_station_name(self) -> str:
        return 'エフエム秋田'

    def get_station_url(self) -> str:
        return 'https://www.fm-akita.co.jp/'

    def get_station_id(self) -> str:
        return 'pu'


class DateFmRadioStation(MtmDefaultRadioStation):
    """Date fm
    """
    tag_key: str = '771fm'

    def get_radio_station_name(self) -> str:
        return 'Date fm'

    def get_station_url(self) -> str:
        # noinspection HttpUrlsUsage
        return 'http://771.fm/smp/'

    def get_station_id(self) -> str:
        return 'ju'

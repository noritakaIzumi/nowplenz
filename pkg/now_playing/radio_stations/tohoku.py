from now_playing.radio_stations import MtmDefaultRadioStation


class FmAomoriRadioStation(MtmDefaultRadioStation):
    """エフエム青森
    """
    tag_key: str = 'afb'

    def get_radio_station_name(self) -> str:
        return 'エフエム青森'

    def get_station_url(self) -> str:
        return 'https://afb.co.jp/'

    def get_station_id(self) -> str:
        return 'wu'


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


class FmIwateRadioStation(MtmDefaultRadioStation):
    """エフエム岩手
    """
    tag_key: str = 'fmii'

    def get_radio_station_name(self) -> str:
        return 'エフエム岩手'

    def get_station_url(self) -> str:
        return 'https://www.fmii.co.jp/'

    def get_station_id(self) -> str:
        return 'qu'


class FmYamagataRadioStation(MtmDefaultRadioStation):
    """エフエム山形
    """
    tag_key: str = 'rfm'

    def get_radio_station_name(self) -> str:
        return 'エフエム山形'

    def get_station_url(self) -> str:
        return 'https://rfm.co.jp/'

    def get_station_id(self) -> str:
        return 'ev'


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


class FmFukushimaRadioStation(MtmDefaultRadioStation):
    """ふくしま FM
    """
    tag_key: str = 'fmf'

    def get_radio_station_name(self) -> str:
        return 'ふくしま FM'

    def get_station_url(self) -> str:
        return 'https://www.fmf.co.jp/'

    def get_station_id(self) -> str:
        return 'tv'

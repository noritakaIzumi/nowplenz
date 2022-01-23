from inspect import isclass
from typing import Dict, Type

from now_playing.core import AbstractRadioStation
import now_playing.radio_stations.kinki as kinki
import now_playing.radio_stations.kanto as kanto
import now_playing.radio_stations.tohoku as tohoku

RADIO_STATION_MAP: Dict[str, Type[AbstractRadioStation]] = {}
for region in [tohoku, kanto, kinki]:
    for attr in dir(region):
        target = getattr(region, attr)
        if isclass(target) and getattr(target, 'tag_key', '') != '':
            target: Type[AbstractRadioStation]
            RADIO_STATION_MAP[target.tag_key] = target

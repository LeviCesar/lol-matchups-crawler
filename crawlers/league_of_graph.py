from typing_extensions import Self
import requests
import re

from enums.lanes import Lanes


class LeagueOfGraph:
    def __init__(self) -> None:
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.url_base = 'https://www.leagueofgraphs.com'
        self._response: requests.Response = None

    @staticmethod
    def get_lane(lane: str) -> str:
        lane = getattr(Lanes, lane.upper())
        assert lane, 'lane not found!'
        return lane.value

    def matchups_page(self, *, champion: str, lane: str) -> Self:
        lane = self.get_lane(lane)
        url = self.url_base + f'/champions/counters/{champion}/{lane}'
        headers = {
            'Cookie': 'lolg_euconsent=nitro'
        }
        headers.update(self.base_headers)

        self._response = requests.get(url=url, headers=headers)
        return self

    def _get_matchups_best_with_from_html(self) -> list:
        assert self._response.text, 'response not found'

        table_infos = re.findall(r'is best with.*?<table.*?>(.*?)</table', self._response.text, flags=re.DOTALL)
        matchups = re.findall(r'<span class=\"name\">(.*?)<\/span>.*?<progressBar data-value=\"(.*?)\"', table_infos[0], flags=re.DOTALL)
        return matchups

    def get_matchups_best_with(self) -> list[tuple]:
        return self._get_matchups_best_with_from_html()

import requests

from app.adapter.league_of_legend.schema import (
    LeagueOutput,
    LeagueOutputItem,
    RiotAccountInput,
    RiotAccountOutput,
    SummonerOutput,
)
from app.core.constants import RIOT_API_KEY

HEADERS = {"X-Riot-Token": RIOT_API_KEY}


def get_account_informations(input: RiotAccountInput) -> RiotAccountOutput:
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{input.game_name}/{input.tag_line}"

    response = requests.get(url, headers=HEADERS)

    data = response.json()

    return RiotAccountOutput(**data)


def get_summoner_informations(puuid: str) -> SummonerOutput:
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"

    response = requests.get(url, headers=HEADERS)

    data = response.json()

    return SummonerOutput(**data)


def get_league_informations(summoner_id: str) -> LeagueOutput:
    url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"

    response = requests.get(url, headers=HEADERS)

    data = response.json()

    return LeagueOutput(league=[LeagueOutputItem(**item) for item in data])

from app.core.commands.after_cs_go_form import extract_steam_id


def test_extract_steam_id_with_url():
    url = "https://steamcommunity.com/profiles/76561198088442493/"

    result = extract_steam_id(url)

    assert result == "76561198088442493"


def test_extract_steam_id_with_id():
    steam_id = "76561198088442493"

    result = extract_steam_id(steam_id)

    assert result == steam_id

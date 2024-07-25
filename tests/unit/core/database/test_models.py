from datetime import datetime

import pytest

from app.core.database.models import RiotScore


@pytest.fixture
def default_kwargs():
    return {"wins": 0, "losses": 0, "created_at": datetime.now(), "riot_account_id": 1}


def test_riot_score_order_eq(default_kwargs):
    first_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )
    second_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )

    assert first_score == second_score


def test_riot_score_order_ne(default_kwargs):
    first_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )
    second_score = RiotScore(
        tier="DIAMOND", rank="II", leaguePoints=100, **default_kwargs
    )

    assert first_score != second_score


def test_riot_score_order_lt(default_kwargs):
    first_score = RiotScore(tier="SILVER", rank="I", leaguePoints=100, **default_kwargs)
    second_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )

    assert first_score < second_score


def test_riot_score_order_le(default_kwargs):
    first_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )
    second_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )

    assert first_score <= second_score


def test_riot_score_order_gt(default_kwargs):
    first_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )
    second_score = RiotScore(
        tier="SILVER", rank="I", leaguePoints=100, **default_kwargs
    )

    assert first_score > second_score


def test_riot_score_sorted_with_multiple_scores(default_kwargs):
    first_score = RiotScore(
        tier="DIAMOND", rank="I", leaguePoints=100, **default_kwargs
    )
    second_score = RiotScore(
        tier="SILVER", rank="I", leaguePoints=100, **default_kwargs
    )
    third_score = RiotScore(tier="GOLD", rank="I", leaguePoints=100, **default_kwargs)

    scores = [first_score, second_score, third_score]
    scores.sort()

    assert scores == [second_score, third_score, first_score]

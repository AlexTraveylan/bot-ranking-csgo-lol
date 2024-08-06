from datetime import datetime

import pytest

from app.core.database.riots_models import RiotScore


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


def test_riot_score_sorted_ranking_in_real_situation(default_kwargs):
    bronze_1_59_LP = RiotScore(
        tier="BRONZE", rank="I", leaguePoints=59, **default_kwargs
    )

    iron_III_17_LP = RiotScore(
        tier="IRON", rank="III", leaguePoints=17, **default_kwargs
    )

    silver_II_7_LP = RiotScore(
        tier="SILVER", rank="II", leaguePoints=7, **default_kwargs
    )

    silver_IV_91_LP = RiotScore(
        tier="SILVER", rank="IV", leaguePoints=91, **default_kwargs
    )

    scores = [bronze_1_59_LP, iron_III_17_LP, silver_II_7_LP, silver_IV_91_LP]
    sorted_score = []

    for index, score in enumerate(sorted(scores, reverse=True)):
        sorted_score.append((index + 1, score))

    assert sorted_score[0] == (1, silver_II_7_LP)
    assert sorted_score[1] == (2, silver_IV_91_LP)
    assert sorted_score[2] == (3, bronze_1_59_LP)
    assert sorted_score[3] == (4, iron_III_17_LP)

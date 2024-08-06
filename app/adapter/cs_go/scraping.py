import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.adapter.cs_go.schemas import CsStatsInfoSchema, StatsPossibles
from app.adapter.exception.bot_exception import CsGoScrapingException

logger = logging.getLogger(__name__)

BASE_URL = "https://csstats.gg/player/"


def make_stats_url(player_id: str) -> str:
    return f"{BASE_URL}{player_id}#/"


def get_html_soup(player_id: str) -> BeautifulSoup:
    url = make_stats_url(player_id)
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rank"))
        )
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

    except Exception as e:
        logger.exception(e)
        raise CsGoScrapingException("An error occurred while opening the page") from e
    finally:
        driver.quit()

    return soup


def get_actual_rank(soup: BeautifulSoup) -> int:
    try:
        rank_divs = soup.find_all("div", class_="rank")

        for rank_div in rank_divs:
            cs2rating_div = rank_div.find("div", class_="cs2rating")
            span = cs2rating_div.find("span")
            rating_text = span.get_text(strip=True)

            return int(rating_text.replace(",", ""))

    except Exception as e:
        logger.exception(e)
        raise CsGoScrapingException("It was not possible to get the rank") from e


def get_best_rank(soup: BeautifulSoup) -> int:
    try:
        best_rank_divs = soup.find_all("div", class_="best")
        for best_rank_div in best_rank_divs:
            cs2rating_div = best_rank_div.find("div", class_="cs2rating")
            span = cs2rating_div.find("span")
            rating_text = span.get_text(strip=True)

            return int(rating_text.replace(",", ""))

    except Exception as e:
        logger.exception(e)
        raise CsGoScrapingException("It was not possible to get the best rank") from e


def get_player_name(soup: BeautifulSoup) -> str:
    try:
        player_name_div_by_id = soup.find("div", id="player-name")

        return player_name_div_by_id.get_text(strip=True)

    except Exception as e:
        logger.exception(e)
        raise CsGoScrapingException("It was not possible to get the player name") from e


def get_player_stats(soup: BeautifulSoup) -> StatsPossibles:
    try:
        total_stat_divs = soup.find_all("div", class_="total-stat")

        stats: StatsPossibles = {}
        for div in total_stat_divs:
            label = div.find("span", class_="total-label")
            value = div.find("span", class_="total-value")
            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                stats[label_text] = int(value_text)

        return stats

    except Exception as e:
        logger.exception(e)
        raise CsGoScrapingException(
            "It was not possible to get the player stats"
        ) from e


def get_player_info(player_id: str) -> CsStatsInfoSchema:
    soup = get_html_soup(player_id)
    rating = get_actual_rank(soup)
    best_rating = get_best_rank(soup)
    player_name = get_player_name(soup)
    stats = get_player_stats(soup)

    try:
        return CsStatsInfoSchema(
            name=player_name,
            wins=stats["Won"],
            losses=stats["Lost"],
            ties=stats["Tied"],
            rank=rating,
            best_rank=best_rating,
            kills=stats["Kills"],
            deaths=stats["Deaths"],
            assists=stats["Assists"],
            headshots=stats["Headshots"],
            damage=stats["Damage"],
        )
    except Exception as e:
        logger.exception(e)
        raise CsGoScrapingException(
            "It was not possible to parse the player info from scraped data"
        ) from e


if __name__ == "__main__":
    IBUSHIN_ID = "76561198088442493"
    data = get_player_info(IBUSHIN_ID)
    print(data)

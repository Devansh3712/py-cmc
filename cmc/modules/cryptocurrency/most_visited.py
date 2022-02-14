#!/usr/bin/env python

"""Module for fetching data of Cryptocurrencies which were the most
visited in the last 24 hours on CoinMarketCap website.
Data is scraped through Selenium (to load JavaScript components) and
BeautifulSoup (to parse website data).
"""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional, Tuple
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass


class MostVisited(CMCBaseClass):
    """Class for scraping the data of CryptoCurrencies that appear
    in the most visited table."""

    def __init__(self, proxy: Optional[str] = None) -> None:
        """
        Args:
            proxy (Optional[str], optional): Proxy to be used for Selenium and
            requests Session. Defaults to None.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/most-viewed-pages/"

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the table from most visited CryptoCurrencies page data
        and return the scraped data.

        Raises:
            InvalidCryptoCurrencyURL: Raised when the URL is
            not valid.

        Returns:
            bs4.BeautifulSoup: Scraped page data.
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.driver_options,
            service_log_path=os.devnull,
        )
        driver.get(self.base_url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        result = driver.find_element(
            By.XPATH,
            '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody',
        )
        page_data = result.get_attribute("innerHTML")
        driver.quit()
        soup = BeautifulSoup(page_data, features="lxml")
        return soup

    @property
    def get_data(self) -> Dict[int, Dict[str, Any]]:
        """Scrape the CryptoCurrencies which are the most visited in the
        last 24 hours.

        Returns:
            Dict[str, Any]: Scraped data of trending CryptoCurrencies.
        """
        most_visited: Dict[int, Dict[str, Any]] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for num, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[2].find("p", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = (
                td[2].find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text
            )
            cmc_link: str = td[2].find("a", class_="cmc-link")["href"]
            try:
                price: str = td[3].find("div", class_="sc-131di3y-0 cLgOOr").text
            except:
                price: str = td[3].span.text  # type: ignore
            try:
                if td[4].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_24h: Tuple[str, ...] = (
                        "down",
                        td[4].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_24h: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[4].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                if td[5].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_7d: Tuple[str, ...] = (
                        "down",
                        td[5].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_7d: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[5].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                if td[6].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_30d: Tuple[str, ...] = (
                        "down",
                        td[6].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_30d: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[6].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                market_cap: str = td[7].find("p", class_="sc-1eb5slv-0 bZMzMD").text
            except:
                market_cap: str = td[7].text  # type: ignore
            volume_24h: str = td[8].text
            most_visited[num + 1] = {
                "name": name,
                "symbol": symbol,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "price": price,
                "percent_24h": percent_24h,
                "percent_7d": percent_7d,
                "percent_30d": percent_30d,
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "timestamp": datetime.now(),
            }
        return most_visited

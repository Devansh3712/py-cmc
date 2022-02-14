#!/usr/bin/env python

"""Module for fetching data of Cryptocurrencies which were the top gainers
in the last 24 hours on CoinMarketCap website.
Data is scraped through Selenium (to load JavaScript components) and
BeautifulSoup (to parse website data).
"""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass


class TopGainers(CMCBaseClass):
    """Class for scraping the data of CryptoCurrencies that appear
    in the top gainers table."""

    def __init__(self, proxy: Optional[str] = None) -> None:
        """
        Args:
            proxy (Optional[str], optional): Proxy to be used for Selenium and
            requests Session. Defaults to None.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/gainers-losers/"

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the gainers table from gainers-losers page data
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
            '//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody',
        )
        page_data = result.get_attribute("innerHTML")
        driver.quit()
        soup = BeautifulSoup(page_data, features="lxml")
        return soup

    @property
    def get_data(self) -> Dict[int, Dict[str, Any]]:
        """Scrape the CryptoCurrencies which are the top gainers in the
        last 24 hours.

        Returns:
            Dict[int, Dict[str, Any]]: Scraped data of top gaining
            CryptoCurrencies.
        """
        top_gainers: Dict[int, Dict[str, Any]] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for num, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[1].find("p", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = (
                td[1].find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text
            )
            rank: int = int(td[0].find("p", class_="sc-1eb5slv-0 bSDVZJ").text)
            cmc_link: str = td[1].find("a", class_="cmc-link")["href"]
            price: str = td[2].span.text
            percentage: str = td[3].find("span", class_="sc-15yy2pl-0 kAXKAX").text
            volume_24h: str = td[4].text
            top_gainers[num + 1] = {
                "name": name,
                "symbol": symbol,
                "rank": rank,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "price": price,
                "percentage": percentage,
                "volume_24h": volume_24h,
                "timestamp": datetime.now(),
            }
        return top_gainers
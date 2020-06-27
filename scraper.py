import csv
from datetime import date, datetime, timedelta
import logging
from os.path import exists
import time
from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag
import requests
from requests.models import Response


class Entry:
    """ブックマークエントリー
    """

    def __init__(self, contents: Tag) -> None:
        link = contents.select_one("h3.entrylist-contents-title > a")

        # title
        self.title: str = link["title"]
        # link
        self.link: str = link["href"]

        # bookmarked users
        self.users: int = int(
            contents.select_one(".entrylist-contents-users span").text
        )
        # domain
        self.domain: str = contents.select_one(
            ".entrylist-contents-domain > a > span"
        ).text
        # description
        self.description: str = contents.select_one(
            "p.entrylist-contents-description"
        ).text
        # category
        self.category: str = contents.select_one(
            "li.entrylist-contents-category > a"
        ).text
        # date
        self.date: datetime = datetime.strptime(
            contents.select_one("li.entrylist-contents-date").text, "%Y/%m/%d %H:%M"
        )

        # tags
        self.tags = [
            content.text for content in contents.select("ul.entrylist-contents-tags a")
        ]

    def __repr__(self):
        return f"{self.title}, {self.link}"


def write_to_csv(_date: str, entry_contents: List[Entry]):
    fieldnames = [
        "title",
        "link",
        "users",
        "domain",
        "description",
        "category",
        "date",
        "tags",
    ]

    with open(f"out/{_date}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames)

        for entry_content in entry_contents:
            writer.writerow(Entry(entry_content).__dict__)


def fetch_data(_date: str) -> ResultSet:
    url: str = f"https://b.hatena.ne.jp/hotentry/all/{_date}"
    response: Response = requests.get(url)
    response.raise_for_status()
    bs: BeautifulSoup = BeautifulSoup(response.text, features="html.parser")
    entry_contents: ResultSet = bs.select(".entrylist-contents")

    return entry_contents


def main():
    today = date.today()

    for i in range(1, 30 * 6 + 1):
        day: date = today - timedelta(days=i)
        _date: str = day.strftime("%Y%m%d")

        if exists(f"out/{_date}.csv"):
            logging.info(f"Entry data exists: {_date}, Skip.")
            continue

        logging.info(f"Download entry data: {_date}")
        entry_contents = fetch_data(_date)
        write_to_csv(_date, entry_contents)

        time.sleep(0.5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()

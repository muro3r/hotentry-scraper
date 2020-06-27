import csv
from datetime import date, datetime, timedelta
from typing import List

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
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

    with open(f"{_date}.csv", "w") as f:
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
    yesterday = today - timedelta(days=1)

    _date: str = (yesterday).strftime("%Y%m%d")
    entry_contents = fetch_data(_date)
    write_to_csv(_date, entry_contents)


if __name__ == "__main__":
    main()

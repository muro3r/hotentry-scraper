# %%
import csv
from datetime import datetime

from bs4 import BeautifulSoup, ResultSet, Tag
import requests
from requests.models import Response

date: str = "20200619"

url: str = f"https://b.hatena.ne.jp/hotentry/all/{date}"
response: Response = requests.get(url)
response.raise_for_status()
bs: BeautifulSoup = BeautifulSoup(response.text, features="html.parser")
entry_contents: ResultSet = bs.select(".entrylist-contents")
# 17-


# %%


class Entry:
    def __init__(self, contents: Tag) -> None:
        # title
        self.title: str = contents.select_one("h3.entrylist-contents-title > a")[
            "title"
        ]
        # link
        self.link: str = contents.select_one("h3.entrylist-contents-title > a")["href"]
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


# %%

# ec = entry_contents[0]
# # title
# ec.select_one("h3.entrylist-contents-title > a")["title"]
# # link
# ec.select_one("h3.entrylist-contents-title > a")["href"]
# # bookmarked users
# ec.select_one(".entrylist-contents-users span").text
# # domain
# ec.select_one(".entrylist-contents-domain > a > span").text
# # description
# ec.select_one("p.entrylist-contents-description").text
# # category
# ec.select_one("li.entrylist-contents-category > a").text
# # date
# ec.select_one("li.entrylist-contents-date").text
# # tags
# [e.text for e in ec.select("ul.entrylist-contents-tags a")]

# %%

# entries = []
# for entry_content in entry_contents:
#     entry = Entry(entry_content)

#     entries.append(entry)


# %%
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

with open(f"{date}.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames)

    for entry_content in entry_contents:
        writer.writerow(Entry(entry_content).__dict__)

# %%

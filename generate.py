import pandas as pd
import requests
import configparser
from jinja2 import Environment, FileSystemLoader

config = configparser.ConfigParser()
config.read("config.ini")
good_reads_api_key = config["goodreads.com"]["key"]

books_df = pd.read_excel("./input/Free+English+textbooks.xlsx")
grouped_books_df = books_df.groupby(["English Package Name"])

loader = FileSystemLoader(searchpath="./templates/")
env = Environment(loader=loader)
template = env.get_template("index.html")

isbn_hyphen_maps = [{}, {}]
isbn_review_map = {}

for book in books_df.iterrows():
    isbn_hyphen_maps[0][book[1]["Print ISBN"]] = book[1]["Print ISBN"].replace('-', '')
    isbn_hyphen_maps[1][book[1]["Electronic ISBN"]] = book[1]["Electronic ISBN"].replace('-', '')
for map in isbn_hyphen_maps:
    response = requests.get("https://www.goodreads.com/book/review_counts.json?isbns=" + ','.join(map.values()) + 'key=' + good_reads_api_key)
    for review in response.json()["books"]:
        isbn_review_map[review["isbn13"]] = review

grouped_books = {}

for group, books in grouped_books_df:
    grouped_books[group] = []
    for book in books.iterrows():
        book[1]["goodreads_review"] = isbn_review_map.get(isbn_hyphen_maps[0][book[1]["Print ISBN"]], isbn_review_map.get(isbn_hyphen_maps[1][book[1]["Electronic ISBN"]], None))
        grouped_books[group].append(book)

rendered_template = template.render(grouped_books=grouped_books)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(rendered_template)
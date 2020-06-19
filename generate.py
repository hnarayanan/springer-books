import pandas as pd
import requests
from jinja2 import Environment, FileSystemLoader

good_reads_api_key = input("Enter Good Reads Api Key: ")

books_df = pd.read_excel("./input/Free+English+textbooks.xlsx")
grouped_books_df = books_df.groupby(["English Package Name"])

loader = FileSystemLoader(searchpath="./templates/")
env = Environment(loader=loader)
template = env.get_template("index.html")

isbn_hyphen_map = {}
isbn_review_map = {}
for book in books_df.iterrows():
    isbn_hyphen_map[book[1]["Print ISBN"]] = book[1]["Print ISBN"].replace('-', '')
response = requests.get("https://www.goodreads.com/book/review_counts.json?isbns=" + ','.join(isbn_hyphen_map.values()) + 'key=' + good_reads_api_key)
for review in response.json()["books"]:
    isbn_review_map[review["isbn13"]] = review

grouped_books = {}

for group, books in grouped_books_df:
    grouped_books[group] = []
    for book in books.iterrows():
        book[1]["goodreads_review"] = isbn_review_map.get(isbn_hyphen_map[book[1]["Print ISBN"]], None)
        grouped_books[group].append(book)

rendered_template = template.render(grouped_books=grouped_books)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(rendered_template)

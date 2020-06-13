import pandas as pd
from jinja2 import Environment, FileSystemLoader


books_df = pd.read_excel("./input/Free+English+textbooks.xlsx")
grouped_books_df = books_df.groupby(["English Package Name"])


loader = FileSystemLoader(searchpath="./templates/")
env = Environment(loader=loader)
template = env.get_template("index.html")

grouped_books = {}

for group, books in grouped_books_df:
    grouped_books[group] = []
    for book in books.iterrows():
        grouped_books[group].append(book)

rendered_template = template.render(grouped_books=grouped_books)

with open("index.html", "w") as f:
    f.write(rendered_template)

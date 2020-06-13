import pandas as pd
from jinja2 import Environment, FileSystemLoader


books_df = pd.read_excel("./input/Free+English+textbooks.xlsx")
grouped_books = books_df.groupby(["English Package Name", "Product Type"])

loader = FileSystemLoader(searchpath="./templates/")
env = Environment(loader=loader)
template = env.get_template("index.html")

rendered_template = template.render(grouped_books=grouped_books)

with open("./output/index.html", "w") as f:
    f.write(rendered_template)

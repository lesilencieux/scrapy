#!/usr/bin/python
# coding: utf-8
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import requests


class ScraperTest:
    @staticmethod
    def get_recipe_links(url):
        # Récupérer le code HTML de la page à scraper
        html_doc = requests.get(url, verify=False).text
        # Convertir le code HTML de la page à scrapper en objet BeautifulSOup
        soup = BeautifulSoup(html_doc, 'html.parser')

        links = soup.find_all("a", class_="recipe-card-link")
        return [link.get('href') for link in links]

    @staticmethod
    def get_info_recipe(link):
        def get_ingredient(li_soup):
            try:
                qt = int(li_soup.find("span", class_="recipe-ingredient-qt").text.strip())
            except:
                qt = 0

            name = li_soup.find("span", class_="ingredient").text.strip()
            return {"quantity": qt, "name": name}

        def get_step(index, li_soup):
            step = li_soup.text.strip()
            return {"index": index + 1, "step": step}

        # Récupérer le code HTML de la page à scraper
        html_doc = requests.get(link, verify=False).text

        # Convertir le code HTML de la page à scrapper en objet BeautifulSOup
        soup = BeautifulSoup(html_doc, 'html.parser')

        name = soup.find("h1", class_="main-title").text.strip()
        cooking_time = soup.find("div", class_="recipe-infos__timmings__cooking").text.strip()
        cooking_time = cooking_time.split("\t")[-1]

        preparation_time = soup.find("div", class_="recipe-infos__timmings__preparation").text.strip()
        preparation_time = preparation_time.split(":")[-1].strip()

        quantity = int(soup.find("span", class_="recipe-infos__quantity__value").text.strip())
        tools = soup.find_all("span", class_="recipe-utensil__name")
        tools = [span.text.strip() for span in tools]
        steps = soup.find_all("li", class_="recipe-preparation__list__item")
        steps = [get_step(index, li_soup) for index, li_soup in enumerate(steps)]
        ingredients = soup.find_all("li", class_="recipe-ingredients__list__item")
        ingredients = [get_ingredient(li_soup) for li_soup in ingredients]

        return {
            "name": name,
            "cooking_time": cooking_time,
            "preparation_time": preparation_time,
            "quantity": quantity,
            "tools": tools,
            "steps": steps,
            "ingredients": ingredients
        }

    @staticmethod
    def main():
        url = "https://www.marmiton.org/recettes/selection_afrique.aspx"
        links = ScraperTest.get_recipe_links(url)
        result = [ScraperTest.get_info_recipe(link) for link in links]
        return result


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def hello_world():
    data = ScraperTest.main()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8385", debug=False)

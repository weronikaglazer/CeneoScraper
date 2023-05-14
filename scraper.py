import requests
from bs4 import BeautifulSoup
import json
import os

def get_element(ancestor, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute].strip()
        if selector and attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        None


selectors = {
    "opinion_id": (None,'data-entry-id'),
    "author": ('.user-post__author-name',),
    "recommendation": ('span.user-post__author-recomendation > em',),
    "score": ('.user-post__score-count',),
    "purchased": ('.review-pz',),
    "opinion_date": ('.user-post__published > time:nth-child(1)','datetime'),
    "purchase_date": ('.user-post__published > time:nth-child(2)','datetime'),
    "likes": ('button.vote-yes', 'data-total-vote'),
    "dislikes": ('button.vote-no', 'data-total-vote'),
    "content": ('.user-post__text',),
    "cons": ('div.review-feature__title--negatives ~ div.review-feature__item', None, True),
    "pros": ('div.review-feature__title--positives ~ div.review-feature__item', None, True)
}

# product_code = input(int('Podaj kod produktu: ')) 
product_code = '95733300'
url = f'https://www.ceneo.pl/{product_code}#tab=reviews'

opinions_all = []

while url:
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        page_dom = BeautifulSoup(response.text, 'html.parser')
        opinions = page_dom.select('div.js_product-review')
        for opinion in opinions:
            single_opinion = {}
            for key, value in selectors.items():
                single_opinion[key] = get_element(opinion, *value)
                
            opinions_all.append(single_opinion)
    try:
        url = 'https://www.ceneo.pl' + get_element(page_dom, 'a.pagination__next', 'href')
    except TypeError: 
        url = None
if not os.path.exists("./opinions"):
    os.mkdir("./opinions")
with open(f"opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(opinions_all, jf, indent=4, ensure_ascii=False)



products = [f for f in os.listdir("./opinions") if os.isfile(join("./opinions", f))]
print(products)
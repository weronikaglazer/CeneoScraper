import requests
from bs4 import BeautifulSoup
import json

# product_code = input(int('Podaj kod produktu: '))
product_code = '95733300'
url = f'https://www.ceneo.pl/{product_code}#tab=reviews'

response = requests.get(url)
if response.status_code == requests.codes.ok:
    page_dom = BeautifulSoup(response.text, 'html.parser')
    opinions = page_dom.select('div.js_product-review')
    
    opinions_all = []
    for opinion in opinions:
        single_opinion = {
            "opinion_id": opinion['data-entry-id'],
            "author": opinion.select_one('.user-post__author-name').text.strip(),
            "recommendation": opinion.select_one('span.user-post__author-recomendation > em').text.strip(),
            "score": opinion.select_one('.user-post__score-count').text.strip(),
            "purchased": opinion.select_one('.review-pz').text.strip(),
            "opinion_date": opinion.select_one('.user-post__published > time:nth-child(1)')['datetime'].strip(),
            "purchase_date": opinion.select_one('.user-post__published > time:nth-child(2)')['datetime'].strip(),
            "likes": opinion.select_one('button.vote-yes')['data-total-vote'].strip(),
            "dislikes": opinion.select_one('button.vote-no')['data-total-vote'].strip(),
            "content": opinion.select_one('.user-post__text').text.strip(),
            "cons": [tag.text.strip() for tag in opinion.select('div.review-feature__title--negatives ~ div.review-feature__item')],
            "pros": [tag.text.strip() for tag in opinion.select('div.review-feature__title--positives ~ div.review-feature__item')]
        }
        opinions_all.append(single_opinion)
    
    print(json.dumps(opinions_all, indent=4, ensure_ascii=False))

    
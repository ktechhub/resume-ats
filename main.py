from collections import Counter
import requests
import spacy
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url = input('Enter job link: ')
page = requests.get(url)
html = page.text

soup = BeautifulSoup(html, 'html.parser')
title = soup.find('h1').string
company = soup.find('a', class_='topcard__org-name-link topcard__flavor--black-link').string.replace("\\n", "").strip()
content = soup.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5')
body_string = ''
for x in iter(content.stripped_strings):
    body_string = body_string + x.lower()
    
nlp = spacy.load('en_core_web_sm')
doc = nlp(body_string)
nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
noun_freq = Counter(nouns)
common_nouns = noun_freq.most_common(25)


noun_list, noun_occurance = zip(*common_nouns)
plt.figure(0)  # Specify differnt figures
plt.barh(noun_list, noun_occurance)
plt.title(f'{title} @ {company}')
plt.ylabel('Word')
plt.xlabel('Occurance')
plt.tight_layout()  # add padding
plt.savefig(f'{title}.png')
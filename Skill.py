import requests
from bs4 import BeautifulSoup

def make_str_searchable(s):
    return s.replace(' ', '%20')
    
def get_wiki_url(s):
    return 'http://wiki-en.guildwars2.com/wiki/Special:Search/' + make_str_searchable(s)
    
def get_skill_id(s):
    wiki_url = get_wiki_url(s)
    r = requests.get(wiki_url)
    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        api_tag = soup.find('a', class_='external text')
        if api_tag is not None:
            return api_tag['href']

    return None
    
def get_skill_json(api_url):
    if api_url is not None:
        r = requests.get(api_url)

        if r.ok and isinstance(r.json(), list):
            return r.json()[0]

    return None
import requests
from bs4 import BeautifulSoup

class Skill:
    def __init__(self, skill_name):
        self.skill_name = skill_name
        self.wiki_url = self._get_wiki_url()
        self.api_url = self._get_skill_id()
        self.skill_json = self._get_skill_json()

    def make_str_searchable(self, s):
        return s.replace(' ', '%20')
    
    def _get_wiki_url(self):
        return 'http://wiki-en.guildwars2.com/wiki/Special:Search/' + self.make_str_searchable(self.skill_name)
    
    def _get_skill_id(self):
        r = requests.get(self.wiki_url)
        if r.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

            api_tag = soup.find('a', class_='external text')
            if api_tag is not None:
                return api_tag['href']

        return None
    
    def _get_skill_json(self):
        if self.api_url is not None:
            r = requests.get(self.api_url)

            if r.ok and isinstance(r.json(), list):
                return r.json()[0]

        return None

    def __repr__(self):
        repr = '\n'.join([f'Name: {self.skill_name}',
                          f'Description: {self.skill_json["description"] if self.skill_json is not None else ""}',
                          f'Icon: {self.skill_json["icon"] if self.skill_json is not None else ""}',
                          f'Chat Code: {self.skill_json["chat_link"] if self.skill_json is not None else ""}'])
        return repr

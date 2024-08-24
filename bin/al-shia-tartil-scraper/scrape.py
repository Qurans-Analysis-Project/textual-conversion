from typing import List, Dict
from bs4 import BeautifulSoup
import asyncio
from aiohttp import ClientSession
from models import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from json import dumps


async def get_recitation_names()-> Dict[str,str]:
    
    RECITATIONS_URL = 'https://quran.al-shia.org/en/tartil/'
    recitations: Dict[str,str] = {}
    async with ClientSession() as session:
        async with session.get(RECITATIONS_URL) as r:
            html = await r.content.read()
            soup = BeautifulSoup(html, 'html.parser')
            reciters_select = soup.find(attrs={'name':'gari'})
            
            for option in reciters_select.children:
                if isinstance(option, str):
                    continue
                if option.get('value') == '0':
                    continue
                recitations[option.get('value')] = option.text
    
    return recitations


def text_to_verses(text: str) -> Dict[int, str]:
    out: Dict[int, str] = {}
    verses = text.replace('»','').replace('«','').split('\n')
    for verse in verses:
        while True:
            # pop leftmost
            char = verse[0]
            text = verse[1:]
            if char.isdecimal():
                out[char] = text.strip()
    return out
    

def save_recitation(recitation: Recitation):
    out_path = Path('generated/json/al-shia.org/al-shia.json')
    



async def main():

    recitation_names = await get_recitation_names()

    browser_options = webdriver.FirefoxOptions()
    browser_options.add_argument("--headless=new")
    browser = webdriver.Firefox(options=browser_options)

    for web_name, name in recitation_names.items():
        chapters = {}
        recitation = Recitation(
            chapters=chapters
        )

        # Get each chapter
        for chapter_number in range(1,115):

            chapter_url = f'https://quran.al-shia.org/en/tartil/quran.htm?sore={chapter_number:03}&{web_name}'
            browser.get(chapter_url)
            browser.implicitly_wait(2)
            text: str = browser.execute_script('return document.querySelectorAll("marquee")[0].innerText')
            verses = text_to_verses(text)
            ch_name = browser.execute_script('return document.querySelector("body > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr:nth-child(3) > td > font").innerText')
            chapters[chapter_number] = Chapter(
                name=ch_name,
                num_verses=len(verses),
                verses=verses
            )

        save_recitation(recitation)

        # Only do one recitation. Turns out they're not the 
        # same as narration.
        break




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
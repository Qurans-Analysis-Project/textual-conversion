
import asyncio
import aiohttp
from models import Narrator, Difference
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from bs4.element import Tag
from pathlib import Path
import time
from json import dump, JSONEncoder
from enum import Enum


async def export_all_diffs(chapter_diffs: Dict[int,Dict[int,List[Difference]]]):
    """
    given a dictionary where:
    each key is a chapter number and
    the value of the chapter key is a dictionary of verse number keys and
    the value of the verse number keys is the list of Differences in that chapter.
    save these differences to a file
    """

    class customJSONEncoder(JSONEncoder):
        def default(o:Any):
            if isinstance(o, Enum):
                return o.name

    OUTPATH = Path("generated/json/nquran/differences.json")
    with open(OUTPATH, encoding='utf-8') as f:
        dump(chapter_diffs, f, ensure=False, cls=customJSONEncoder)


async def scrape_verse(ch: int, verse: int, url: str) -> List[Difference]:

    def filter_to_disputes(tag):
        return tag.has_attr('class') \
        and "selectquran" in tag['class']

    ret: List[Difference] = []
    VERSE_URL = url
    soup: BeautifulSoup
    time.sleep(.2)
    while True:
        async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97'}) as session:
            async with session.get(VERSE_URL) as response:
                soup = BeautifulSoup(await response.text(), features='lxml')
                if soup.find(class_="blockrwaya") is not None:
                    break
                print(f"Error page on ch:{ch} v:{verse}. Sleeping 5 seconds.")
                time.sleep(5)
        
    disputes = soup.find(class_="blockrwaya").find_all(filter_to_disputes, recursive=False)
    # handle each dispute
    for dispute in disputes:
        dispute: Tag
        verse_content = dispute.find('strong', recursive=False).find('font', recursive=False).get_text(strip=True)
        verse_text = verse_content.split('{')[1].split('}')[0]
        
        # disputed phrase
        temp = dispute.find(class_="selectquran").find('h2', recursive=False)
        temp2 = temp.find('font', recursive=False)
        if temp2:
            disputed_phrase = temp2.find('strong', recursive=False).text
        else:
            disputed_phrase = temp.find('strong', recursive=False).text
        disputed_phrase = disputed_phrase.strip().split('{')[1].split('}')[0]

        # pull each difference for the disputed phrase
        for dif in dispute.find_all(class_='quran-page'):
            dif: Tag
            # pull narrators
            narrs = []
            narrs_tags: List[Tag] = list(dif.find(class_="rawa-list").find('div').children)
            current_narr = ''
            for i, tag in enumerate(narrs_tags):
                if isinstance(tag, str):
                    continue
                if tag.name =='div':
                    narrs.append(Narrator(current_narr.strip()))
                    current_narr = ''
                    continue
                if i == len(narrs_tags)-1:
                    t= tag.text.replace(u'\xa0', u'')
                    current_narr+=f" {t}"
                    narrs.append(Narrator(current_narr.strip()))
                    current_narr = ''
                else:
                    t= tag.text.replace(u'\xa0', u'')
                    current_narr+=f" {t}"

            # pull comment
            comment = dif.find('strong').text

            # generate Differences
            ret.append(Difference(
                chapter_num=ch,
                verse_num=verse,
                verse_text=verse_text,
                disputed_phrase=disputed_phrase,
                narrators=narrs,
                comment=comment
            ))
    return ret


async def scrape_chapter(ch:int) -> Dict[int,List[Difference]]:
    CH_URL = f"https://www.nquran.com/ar/index.php?group=tb1&tpath=2&aya_no=1,1&sorano={ch}&mRwai="
    async with aiohttp.ClientSession() as session:
        async with session.get(CH_URL) as response:

            # scrape each verse
            soup = BeautifulSoup(await response.text(), features='lxml')
            verse_options = soup.find(id="ayano").findAll(name="option")
            awaitables = []
            for option in verse_options:
                verse_val:str = option["value"]
                verse_num = int(verse_val.strip().split(',')[0])
                verse_url = f"https://www.nquran.com/ar/index.php?group=tb1&tpath=2&aya_no={verse_val}&sorano={ch}&mRwai="
                awaitables.append(scrape_verse(ch, verse_num, verse_url))
            results = await asyncio.gather(*awaitables)
            ret = {}
            for i, diffs in enumerate(results):
                ret[i+1] = diffs
            return ret


async def main():
    URL="https://www.nquran.com/ar/index.php?group=tb1&tpath=2&aya_no=1,1&sorano=1&mRwai="
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:

            # scrape each chapter
            soup = BeautifulSoup(await response.text(), features='lxml')
            num_chapters = len(soup.find(id="sorano").findAll(name="option"))
            all_diffs = {}
            for ch_num in range(1,num_chapters):
                ch_diffs =await scrape_chapter(ch_num)
                all_diffs[ch_num] = ch_diffs
            
            # save to file
            export_all_diffs(all_diffs)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(main())
    end = time.time()
    print(f"Completed in: {end-start} seconds")
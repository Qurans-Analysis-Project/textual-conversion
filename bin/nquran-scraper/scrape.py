
import asyncio
import aiohttp
from models import Narrator, Difference
from typing import List, Dict
from bs4 import BeautifulSoup
from pathlib import Path
import time


async def export_all_diffs(chapter_diffs: Dict[int,Dict[int,List[Difference]]]):
    """
    given a dictionary where:
    each key is a chapter number and
    the value of the chapter key is a dictionary of verse number keys and
    the value of the verse number keys is the list of Differences in that chapter.
    save these differences to a file
    """
    OUTPATH = Path("generated/json/nquran/differences.json")
    pass


async def scrape_verse(ch: int, verse: int, url: str) -> List[Difference]:

    def filter_to_disputes(tag):
        return tag.has_attr('class') \
        and "selectquran" in tag['class']

    VERSE_URL = url
    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97'}) as session:
        async with session.get(VERSE_URL) as response:
            soup = BeautifulSoup(await response.text(), features='lxml')
            disputes = soup.find(class_="blockrwaya").find_all(filter_to_disputes, recursive=False)
            # handle each dispute
            for dispute in disputes:
                pass



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
                ret[i] = diffs
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
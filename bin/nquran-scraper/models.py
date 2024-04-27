from dataclasses import dataclass
from enum import Enum
from typing import List

#NOTE: nquran uses fonts: '"Noto Naskh Arabic", arial, sans-serif, helvetica'
# the narrator names and text will not appear the same in unicode as the website
# unless the same font is used.

class Narrator(Enum):
    HAFS_FROM_ASIM="حفص عن عاصم",
    QALUN_FROM_NAFI="قالون عن نافع",
    WARSH_FROM_NAFI="ورش عن نافع",
    AL_BAZZI_FROM_IBN_KATHIR="البزي عن ابن كثير",
    QUNBUL_FROM_IBN_KATHIR="قنبل عن ابن كثير",
    DURI_FROM_ABU_AMR="دوري أبي عمرو",
    AL_SUSI_FROM_ABU_AMR="السوسي عن أبي عمرو",
    HISHAM_FROM_IBN_AMIR="هشام عن ابن عامر",
    IBN_ZAKWAN_FROM_IBN_AMIR="ابن ذكوان عن ابن عامر",
    SHUBAH_FROM_ASIM="شعبة عن عاصم",
    KHALAF_FROM_HAMZAH="خلف عن حمزة",
    KHALLAD_FROM_HAMZAH="خلاد عن حمزة",
    ABU_AL_HARITH_FROM_AL_KISAI="أبو الحارث عن الكسائي",
    AD_DURI_FROM_AL_KISAI="الدوري عن الكسائي",
    IBN_WARDAN_FROM_ABU_JAFAR="ابن وردان عن أبي جعفر",
    IBN_JAMAZ_FROM_ABU_JAFAR="ابن جماز عن أبي جعفر",
    RUWAYS_FROM_YAQUB_AL_HADRAMI="رويس عن يعقوب الحضرمي",
    RUH_FROM_YAQUB_AL_HADRAMI="روح عن يعقوب الحضرمي",
    ISHAQ_AL_WARRAQ_FROM_KHALF_AL_BAZZAR="إسحاق الوراق عن خلف البزار",
    IDRIS_AL_HADDAD_FROM_KHALF_AL_BAZZAR="إدريس الحداد عن خلف البزار",
    THE_REST_OF_THE_NARRATORS="باقي الرواة"

@dataclass
class Difference():
    chapter_num: int
    verse_num: int
    verse_text: str
    disputed_word: str
    narrators: List[Narrator]
    comment: str

    def __init__(self,
        chapter_num: int,
        verse_num: int,
        verse_text: str,
        disputed_phrase: str,
        narrators: List[Narrator] | List[str],
        comment: str
    ):
        self.chapter_num = chapter_num
        self.verse_num = verse_num
        self.verse_text = verse_text
        self.disputed_phrase = disputed_phrase
        self.narrators = []
        for narr in narrators:
            if isinstance(str):
                self.narrators.append(Narrator(narr))
            elif isinstance(Narrator):
                self.narrators.append(narr)
        self.comment = comment
from dataclasses import dataclass
from enum import Enum
from typing import List

#NOTE: nquran uses fonts: '"Noto Naskh Arabic", arial, sans-serif, helvetica'
# the narrator names and text will not appear the same in unicode as the website
# unless the same font is used.

class Narrator(Enum):
    HAFS_FROM_ASIM="حفص عن عاصم"
    QALUN_FROM_NAFI="قالون عن نافع"
    WARSH_FROM_NAFI="ورش عن نافع"
    AL_BAZZI_FROM_IBN_KATHIR="البزي عن ابن كثير"
    QUNBUL_FROM_IBN_KATHIR="قنبل عن ابن كثير"
    DURI_FROM_ABU_AMR="دوري أبي عمرو"
    AL_SUSI_FROM_ABU_AMR="السوسي عن أبي عمرو"
    HISHAM_FROM_IBN_AMIR="هشام عن ابن عامر"
    IBN_ZAKWAN_FROM_IBN_AMIR="ابن ذكوان عن ابن عامر"
    SHUBAH_FROM_ASIM="شعبة عن عاصم"
    KHALAF_FROM_HAMZAH="خلف عن حمزة"
    KHALLAD_FROM_HAMZAH="خلاد عن حمزة"
    ABU_AL_HARITH_FROM_AL_KISAI="أبو الحارث عن الكسائي"
    AD_DURI_FROM_AL_KISAI="الدوري عن الكسائي"
    IBN_WARDAN_FROM_ABU_JAFAR="ابن وردان عن أبي جعفر"
    IBN_JAMAZ_FROM_ABU_JAFAR="ابن جماز عن أبي جعفر"
    RUWAYS_FROM_YAQUB_AL_HADRAMI="رويس عن يعقوب"#"رويس عن يعقوب الحضرمي"
    RUH_FROM_YAQUB_AL_HADRAMI="روح عن يعقوب الحضرمي"
    ISHAQ_AL_WARRAQ_FROM_KHALF_AL_BAZZAR="إسحاق الوراق عن خلف البزار"
    IDRIS_AL_HADDAD_FROM_KHALF_AL_BAZZAR="إدريس الحداد عن خلف البزار"
    YAQUB_IBN_ISHAQ_IBN_ZAID_AL_HADRAMI_ABU_MUHAMMED_AL_BASRI="يعقوب"
    AASIM_IBN_ABI_AN_NAJOOD_ABU_BAKR_AL_ASADI_AL_KUFI="عاصم"
    AL_KISAI_ABU_AL_HASAN_ALI_IBN_HAMZAH_IBN_ABDULLAH_AL_ASADI="الكسائي"
    ABU_MUHAMMAD_KHALAF_IBN_HUSHAM_AL_BAZZAR_AL_ASADI_AL_BAGHDADI_AL_SALHI="خلف العاشر"
    HAMZAH_IBN_HABIB_IBN_UMARA_ABU_UMARA_AL_ZAYYAT_AL_KUFI="حمزة"
    ABU_JAFAR_YAZID_IBN_AL_QAQA_AL_MAKHZUMI_AL_MADANI="أبو جعفر"
    ABDULLAH_IBN_KATHIR_AL_MAKKI="ابن كثير"
    ABU_AMR_ZABAN_IBN_AL_ALA_AL_MAZINI_AL_BASRI="أبو عمرو"
    ABDULLAH_IBN_AMIR_AL_YAHSUBI="ابن عامر"
    NAFI_IBN_ABDURRAHMAN_IBN_ABI_NUAYM_ABU_RUWAYM_AL_MADANI="نافع"
    ABU_AMR_ZABAN_IBN_AL_ALA_AL_MAZINI_AL_BASRI="الدوري عن أبي عمرو"
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
            if isinstance(narr, str):
                self.narrators.append(Narrator(narr))
            elif isinstance(narr, Narrator):
                self.narrators.append(narr)
        self.comment = comment
from fontTools.ttLib.ttFont import TTFont
from fontTools.ttLib.tables.G_S_U_B_ import table_G_S_U_B_
from fontTools.ttLib.tables._g_c_i_d import table__g_c_i_d
from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables.otTables import LookupList
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.merge.cmap import _glyphsAreSame
from argparse import ArgumentParser
from pathlib import Path
from typing import Tuple, List
from hashlib import md5
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import openpyxl


def verify_inputs(inpaths_str: List[str]) -> List[Path]:
    in_type = None
    ret = []
    for inpath in inpaths_str:
        inp = Path(inpath[0])
        if inp.is_dir():
            in_type = 'dir'
            ret.append(inp)
        if in_type is None:
            raise LookupError(f"Argument --source not provided directory. Got {inp.absolute()}")
        if not inp.exists():
            raise FileNotFoundError(f"Argument --source provided file or directory that does not exist. Got {inp.absolute()}")
    return (ret)


def verify_output(outpath: str) -> Workbook:
    outp = Path(outpath[0])
    if outp.is_dir():
        raise FileNotFoundError(f"Argument --out only accepts a path to open/create an xlsx file. Got {outp.absolute()}")
    if not outp.exists():
        wb = Workbook()
        wb.save(outp)
    else:
        wb = openpyxl.open(outp)
    return wb, outp


def init_excel_sheet(wb: Workbook, outpath: Path):
    wb.create_sheet("Intro", index=0)
    sheet: Worksheet = wb["Intro"]
    cell = sheet.cell(row=1, column=1)
    cell.value = "Each distributor receives it's own sheet"
    cell = sheet.cell(row=2, column=1)
    cell.value = "Walking of equivalent glyphs from one distributor to another happens in intermediary sheets."
    cell = sheet.cell(row=3, column=1)
    cell.value = "Each glyph is represented by the md5 of the glyph components, the glyph image, and the names given to this glyph as duplicates are often present with different names."
    cell = sheet.cell(row=4, column=1)
    cell.value = "Each distributor's glyphs initially begin in the unsorted column and then by hand are sorted into distinct groups based on characteristcs such as rasm."
    wb.save(outpath)


if __name__ == '__main__':

    argp = ArgumentParser()
    argp.add_argument("--source",
                      help="""The directory path for multiple .ttf font files.
                      The allowed structure is .../distributor-name/narrator-names/font-files.[ttf|otf]
                      Where each narrator can have many font files and
                      each distributor can have many narrators
                      Searches recursively.""",
                      required=True,
                      action='append',
                      nargs='+'
                      )
    argp.add_argument("--out-dir",
                      help="""The path to the output directory.""",
                      required=True,
                      nargs=1
                      )
    ns = argp.parse_args()

    # Verify Args
    inpaths = verify_inputs(ns.source)
    workbook, out_path = verify_output(ns.out_dir)

    init_excel_sheet(workbook, out_path)

    with open("source/qurancomplex.gov.sa/UthmanicBazzi_V20/UthmanicBazzi V20.ttf", 'rb') as f:
        font1 = TTFont(f, lazy=False)
    #with open("source/qurancomplex.gov.sa/UthmanicHafs1_Ver13/UthmanicHafs1 Ver13.ttf", 'rb') as f:
    with open("generated/font-merging/islamwebdotnet/alhareth/font-0317.ttf", 'rb') as f:
        font2 = TTFont(f, lazy=False)
    font1.ensureDecompiled()
    font2.ensureDecompiled()
    
    glyphset= font1.getGlyphSet()
    for key, val in glyphset.glyphsMapping.glyphs.items():
        val: Glyph
        print(key)
        print(val)
        pen = DecomposingRecordingPen(glyphset)
        val.draw(pen, glyphset.glyfTable)
        pen.value

    1+1
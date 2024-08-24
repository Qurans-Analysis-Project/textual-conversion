from fontTools.ttLib.ttFont import TTFont
from fontTools.ttLib.tables.G_S_U_B_ import table_G_S_U_B_
from fontTools.ttLib.tables._g_c_i_d import table__g_c_i_d
from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables.otTables import LookupList
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.merge.cmap import _glyphsAreSame
from argparse import ArgumentParser
from pathlib import Path
from typing import Tuple, List
from hashlib import md5
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import openpyxl
from PIL import ImageFont, ImageDraw, Image
from collections import defaultdict
from freetype import ft_errors


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
    cell.value = "Each glyph is represented by the glyph image, the md5 of the glyph components, the rasm group name, the ijam group name, the harakat group name, and the set of names given to this glyph."
    cell = sheet.cell(row=4, column=1)
    cell.value = "Each distributor's glyphs initially begin in the unsorted column and then by hand are sorted into distinct groups based on characteristics"
    wb.save(outpath)


if __name__ == '__main__':

    argp = ArgumentParser()
    argp.add_argument("--source",
                      help="""The directory path for multiple .ttf font files.
                      Can be used multiple times!
                      Searches for .ttf & .otf
                      The allowed structure is ...path/to/<distributor-name>
                      The final element in the path must be the distributor name
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

    # NOTE SHOULD BE WRITTEN TO NOT OVERWRITE EXISTING WORK WHEN RUN. MAKE NEW TABS.
    font_files = dict()
    for inpath in inpaths:
        print(inpath)
        font_files[inpath] = list(Path.rglob(inpath,'*.ttf')) + list(Path.rglob(inpath,'*.otf'))
    
    # store output
    all_glyph_rows = dict()
    bad = [] # path, fontfile, name, reason

    for path, fontfiles in font_files.items():
        for fontfile in fontfiles:
            # open
            font = None
            with open(fontfile, 'rb') as f:
                font = TTFont(f, lazy=False)
            #font.ensureDecompiled()

            glyphset = font.getGlyphSet()
            for name, glyf in glyphset.glyfTable.glyphs.items():
                if '.notdef' in name:
                    continue
                glyf: Glyph

                try:
                    # get the instructions
                    pen = DecomposingRecordingPen(glyphset)
                    glyf.draw(pen, glyphset.glyfTable)
                    instructions = pen.value
                    # generate md5 hash
                    hash = md5(usedforsecurity=False)
                    hash.update(str(instructions).encode())
                    md5_hex = hash.hexdigest()

                    # generate the image of the glyph
                    
                    ftpen = FreeTypePen(glyphSet=glyphset)
                    glyf.draw(ftpen, glyfTable=glyphset.glyfTable)
                    glyf_image = ftpen.image(width=0, height=0, contain=True)

                except ft_errors.FT_Exception as e:
                    bad.append((path, fontfile, name, f"{type(e)}:{e}"))
                    continue # don't save data

                # save data
                if md5_hex in all_glyph_rows:
                    names_set: set = all_glyph_rows[md5_hex]['names']
                    names_set.add(name)
                    all_glyph_rows[md5_hex]['names'] = names_set
                else:
                    all_glyph_rows[md5_hex] = {
                        'image':glyf_image,
                        'names':set([name])
                    }

        # save out to excel sheet

            # save PIL image
            # https://stackoverflow.com/questions/10888969/insert-image-in-openpyxl
            1+1


    with open("source/qurancomplex.gov.sa/UthmanicBazzi_V20/UthmanicBazzi V20.ttf", 'rb') as f:
        font1 = TTFont(f, lazy=False)
    #with open("source/qurancomplex.gov.sa/UthmanicHafs1_Ver13/UthmanicHafs1 Ver13.ttf", 'rb') as f:
    with open("generated/font-merging/islamwebdotnet/alhareth/font-0317.ttf", 'rb') as f:
        font2 = TTFont(f, lazy=False)
    font1.ensureDecompiled()
    font2.ensureDecompiled()
    
    glyphset= font1.getGlyphSet()
    for key, val in glyphset.glyfTable.glyphs.items():
        val: Glyph
        print(key)
        print(val)
        pen = DecomposingRecordingPen(glyphset)
        val.draw(pen, glyphset.glyfTable)
        pen.value

    1+1
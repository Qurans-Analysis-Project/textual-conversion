from pypdf import PdfReader
from argparse import ArgumentParser
#from os.path import isdir, isfile
from pathlib import Path
from typing import Tuple, List
from json import dumps


def verify_input(inpath: str) -> Tuple[Path,str]:
    in_type = None
    inp = Path(inpath)
    if inp.is_dir():
        in_type = 'dir'
    elif inp.is_file():
        in_type = 'file'
    if in_type is None:
        raise LookupError(f"Argument --source not provided file or directory. Got {inp.absolute()}")
    if not inp.exists():
        raise FileNotFoundError(f"Argument --source provided file or directory that does not exist. Got {inp.absolute()}")
    return (inp, in_type)


def verify_output(outpath: str) -> Path:
    outp = Path(outpath)
    if not outp.is_dir():
        raise FileNotFoundError(f"Argument --out only accepts a directory path that exists. Got {outp.absolute()}")
    # Add filename to the end
    outp = Path(f"{outp.as_posix()}/fonts.json")
    # Verify output location
    if outp.exists():
        cont = input("WARNING: An output file already exists at this location. Continuing will overwrite this file.\nAre you sure you wish to continue? Y/N ")
        if cont in ('n', 'N'):
            print("Exiting.")
            raise FileExistsError()
    return outp


def pull_fonts(pdf: Path) -> list:
    """
    Pull every fonts in pdf and return them as a tuple
    """
    fonts = set()
    reader = PdfReader(pdf.open('rb'))
    for page in reader.pages:
        fonts.update(page._get_fonts()[1])
        #page.extract_text(visitor_text=visitor_body)
    return list(fonts)


def visitor_body(text, cm, tm, font_dict, font_size):
    print(f"text:{text}")
    print(type(font_dict))


if __name__ == '__main__':

    argp = ArgumentParser()
    argp.add_argument("--source",
                      help="""The directory path for multiple source documents. Searches recursively.
                        Or specify a single file to only parse that file."""
                      )
    argp.add_argument("--out-dir",
                      help="""The path to the output directory."""
                      )
    ns = argp.parse_args()

    # Verify Args
    inpath, in_type = verify_input(ns.source)
    outpath = verify_output(ns.out_dir)
    
    # gather all input PDFS
    all_pdfs: List[Path] = []
    if in_type == "file":
        all_pdfs.append(inpath)
    elif in_type == 'dir':
        all_pdfs.extend([x for x in inpath.rglob('*.pdf')])
    print(f"Found {len(all_pdfs)} PDF(s).")
    
    # Pull all fonts from every pdf
    # stored output
    fonts = {}
    for pdf in all_pdfs:
        fnts = pull_fonts(pdf)
        pdf_source = pdf.parts[-2]
        pdf_name = pdf.parts[-1]
        if pdf_source not in fonts:
            fonts[pdf_source] = {}
        fonts[pdf_source][pdf_name] = fnts
        print(f"{pdf.parts[-2]} {[pdf.parts[-1]]} complete.")
    
    # write out
    outpath.write_text(dumps(fonts))
    print("Complete. Exiting.")

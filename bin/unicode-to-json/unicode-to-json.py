from argparse import ArgumentParser
#from os.path import isdir, isfile
from pathlib import Path
from typing import Tuple, List
from json import dumps

ARABIC_NUMERALS = [
    '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '١٠', '١١', '١٢', '١٣', '١٤', '١٥', '١٦', '١٧', '١٨', '١٩', '٢٠',
    '٢١', '٢٢', '٢٣', '٢٤', '٢٥', '٢٦', '٢٧', '٢٨', '٢٩', '٣٠', '٣١', '٣٢', '٣٣', '٣٤', '٣٥', '٣٦', '٣٧', '٣٨', '٣٩', '٤٠',
    '٤١', '٤٢', '٤٣', '٤٤', '٤٥', '٤٦', '٤٧', '٤٨', '٤٩', '٥٠', '٥١', '٥٢', '٥٣', '٥٤', '٥٥', '٥٦', '٥٧', '٥٨', '٥٩', '٦٠', '٦١',
    '٦٢', '٦٣', '٦٤', '٦٥', '٦٦', '٦٧', '٦٨', '٦٩', '٧٠', '٧١', '٧٢', '٧٣', '٧٤', '٧٥', '٧٦', '٧٧', '٧٨', '٧٩', '٨٠', '٨١', '٨٢',
    '٨٣', '٨٤', '٨٥', '٨٦', '٨٧', '٨٨', '٨٩', '٩٠', '٩١', '٩٢', '٩٣', '٩٤', '٩٥', '٩٦', '٩٧', '٩٨', '٩٩', '١٠٠', '١٠١', '١٠٢', '١٠٣',
    '١٠٤', '١٠٥', '١٠٦', '١٠٧', '١٠٨', '١٠٩', '١١٠', '١١١', '١١٢', '١١٣', '١١٤', '١١٥', '١١٦', '١١٧', '١١٨', '١١٩', '١٢٠', '١٢١', '١٢٢',
    '١٢٣', '١٢٤', '١٢٥', '١٢٦', '١٢٧', '١٢٨', '١٢٩', '١٣٠', '١٣١', '١٣٢', '١٣٣', '١٣٤', '١٣٥', '١٣٦', '١٣٧', '١٣٨', '١٣٩', '١٤٠', '١٤١',
    '١٤٢', '١٤٣', '١٤٤', '١٤٥', '١٤٦', '١٤٧', '١٤٨', '١٤٩', '١٥٠', '١٥١', '١٥٢', '١٥٣', '١٥٤', '١٥٥', '١٥٦', '١٥٧', '١٥٨', '١٥٩', '١٦٠',
    '١٦١', '١٦٢', '١٦٣', '١٦٤', '١٦٥', '١٦٦', '١٦٧', '١٦٨', '١٦٩', '١٧٠', '١٧١', '١٧٢', '١٧٣', '١٧٤', '١٧٥', '١٧٦', '١٧٧', '١٧٨', '١٧٩',
    '١٨٠', '١٨١', '١٨٢', '١٨٣', '١٨٤', '١٨٥', '١٨٦', '١٨٧', '١٨٨', '١٨٩', '١٩٠', '١٩١', '١٩٢', '١٩٣', '١٩٤', '١٩٥', '١٩٦', '١٩٧', '١٩٨',
    '١٩٩', '٢٠٠', '٢٠١', '٢٠٢', '٢٠٣', '٢٠٤', '٢٠٥', '٢٠٦', '٢٠٧', '٢٠٨', '٢٠٩', '٢١٠', '٢١١', '٢١٢', '٢١٣', '٢١٤', '٢١٥', '٢١٦', '٢١٧',
    '٢١٨', '٢١٩', '٢٢٠', '٢٢١', '٢٢٢', '٢٢٣', '٢٢٤', '٢٢٥', '٢٢٦', '٢٢٧', '٢٢٨', '٢٢٩', '٢٣٠', '٢٣١', '٢٣٢', '٢٣٣', '٢٣٤', '٢٣٥', '٢٣٦',
    '٢٣٧', '٢٣٨', '٢٣٩', '٢٤٠', '٢٤١', '٢٤٢', '٢٤٣', '٢٤٤', '٢٤٥', '٢٤٦', '٢٤٧', '٢٤٨', '٢٤٩', '٢٥٠', '٢٥١', '٢٥٢', '٢٥٣', '٢٥٤', '٢٥٥',
    '٢٥٦', '٢٥٧', '٢٥٨', '٢٥٩', '٢٦٠', '٢٦١', '٢٦٢', '٢٦٣', '٢٦٤', '٢٦٥', '٢٦٦', '٢٦٧', '٢٦٨', '٢٦٩', '٢٧٠', '٢٧١', '٢٧٢', '٢٧٣', '٢٧٤',
    '٢٧٥', '٢٧٦', '٢٧٧', '٢٧٨', '٢٧٩', '٢٨٠', '٢٨١', '٢٨٢', '٢٨٣', '٢٨٤', '٢٨٥', '٢٨٦', '٢٨٧', '٢٨٨', '٢٨٩', '٢٩٠', '٢٩١', '٢٩٢', '٢٩٣',
    '٢٩٤', '٢٩٥', '٢٩٦', '٢٩٧', '٢٩٨','٢٩٩', '٣٠٠'
]


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
    return outp


def split_into_chapters(txt: str) -> List[str]:
    chapters = txt.split('سُورَةُ')[1:]
    # .split eliminates the delimiter so have to add back 'سُورَةُ' to the beginning of every chapter
    for i in range(len(chapters)):
        chapters[i] = "سُورَةُ"+chapters[i]
    return chapters


def split_chapter_into_verses(txt:str) -> dict:
    """
    Return a chapter object of form:
    Chapter {
        "name": String,
        "verses": List[Verse]
    }
    Verse object {
        "arabic_num": String
        "text": String,
        "words" List[String]
    }
    """
    ret = {
        'name':'',
        'verses': {}
    }
    # get chapter name/title
    parts = txt.partition("\n")
    name = parts[0]
    ret['name'] = name.strip()
    txt = parts[2]
    txt = txt.replace('\n', '') # remove newlines

    # cycle through each verse
    verse_num = 1
    for i in ARABIC_NUMERALS:
        verse, sep, txt = txt.partition(i)
        verse = verse.replace('\xa0','') # remove hard-space

        # did number exist?
        if sep == '':
            break

        ret['verses'][verse_num] = {
            'arabic_num': sep,
            'text': verse,
            'words': verse.strip().split(' ')
        }
        verse_num += 1
    return ret


# There are exactly 114 counts of: سُورَةُ , in every narraration. They begin at the name of the new chapter. Use this as chapter delimiter
def to_obj(inpath: Path) -> dict:
    ret = {
        'narraration': inpath.name,
        'chapters':{}
    }
    txt: str = doc.read_bytes().decode('utf-8')
    #print( f"nar: {inpath.name} , count of delimiter: { txt.count( 'سُورَةُ' ) }" )
    txt = txt.replace('\r', '') # make newlines only \n instead of \r\n for easier parsing
    txt = txt.replace('\n\n', '\n') # replace any double newlines with single newline
    
    chs = split_into_chapters(txt)
    for i in range(len(chs)):
        ret['chapters'][i+1] = split_chapter_into_verses(chs[i])

    return ret
    
    


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
    
    # gather all input TXT files
    all_txts: List[Path] = []
    if in_type == "file":
        all_txts.append(inpath)
    elif in_type == 'dir':
        all_txts.extend([x for x in inpath.rglob('*.txt')])
    print(f"Found {len(all_txts)} TXT(s).")
    
    # Pull every chapter and verse into a JSON structure
    for doc in all_txts:
        print(f"Parsing: {str(doc)}")
        js = to_obj(doc)
        doc_source = doc.parts[1:]  # get the path to the doc minus the '.source/'
        doc = outpath.joinpath(*doc_source)   # similar path but to .generated/json
        doc = doc.with_suffix('.json')   # change the suffix to .json
        Path( *(doc.parts[:-1]) ).mkdir(parents=True, exist_ok=True) # create parent directory structure if it doesn't already exist
        doc.write_text(dumps(js)) # write out
        print(f"{doc.stem} {doc.name} complete.")

    print("Complete. Exiting.")
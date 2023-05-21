import textract
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
    return outp



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
    
    # gather all input DOC and DOCX
    all_docs: List[Path] = []
    if in_type == "file":
        all_docs.append(inpath)
    elif in_type == 'dir':
        all_docs.extend([x for x in inpath.rglob('*.docx')])
    print(f"Found {len(all_docs)} DOC(X)(s).")
    
    # Pull all text from each doc
    # stored output
    for doc in all_docs:
        print(f"Parsing: {str(doc)}")
        txt = textract.process(str(doc), output_encoding='utf-8')
        doc_source = doc.parts[1:]  # get the path to the doc minus the '.source/'
        doc = outpath.joinpath(*doc_source)   # similar path but to .generated/text
        doc = doc.with_suffix('.txt')   # change the suffix to .txt
        Path( *(doc.parts[:-1]) ).mkdir(parents=True, exist_ok=True) # create parent directory structure if it doesn't already exist
        doc.write_bytes(txt) # write out
        print(f"{doc.stem} {doc.name} complete.")

        

    print("Complete. Exiting.")
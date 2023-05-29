# textual-conversion
There are reportedly more than 30 different narrarations and readings in existance in physical copies but these are not readily usable for automated textual analysis. Electronic versions of the many narrarations and readings are difficult to find. The source documents possessed are PDFs, DOC, and DOCX. The PDFs use various font encodings and so are still not readily available for automated analysis. This repo seeks to provide these digital documents for distribution and convert these documents into UTF-8and JSON for easier analysis.

Both the source PDFs, DOC, and DOCX and the generated UTF-8/Unicode and JSON are free to distribute and reuse.

## source
The source folder provides the Quran narrarations and readings collected in their received PDF, DOC, or DOCX form.

## generated
The generated folder provides the resulting UTF-8 texts for each Quran. These will be in TXT files.
It also provides the parsed JSON files for each narraration. Breaking down by chapter, chapter title, verses, and individual words. These will be JSON files.

## bin
The scripts performing the parsing and generation

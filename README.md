# textual-conversion
There are reportedly more than 30 different narrarations and readings in existance in physical copie but these are readily usable for automated textual analysis. Electronic versions of the many narrarations and readings are difficult to find. The source documents possessed are PDFs using various font encodings and so are still not readily available for automated analysis. This repo seeks to provide these PDF documents for distribution and convert these PDFs into UTF-8 documents for easier analysis.

Both the source PDFs and the generated UTF-8 are free to distribute.

## source
The source folder provides the Quran narrarations and readings collected in their received PDF, DOC, or DOCX form.

## generated
The generated folder provides the resulting UTF-8 texts for each Quran. These will be in TXT files.
It also provides the parsed JSON files for each narraration. Breaking down by chapter, chapter title, verses, and individual words. These will be JSON files.

## bin
The scripts performing the parsing and generation

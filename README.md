# textual-conversion
There are reportedly more than 30 different narrarations and readings in existance in physical copie but these are readily usable for automated textual analysis. Electronic versions of the many narrarations and readings are difficult to find. The source documents possessed are PDFs using various font encodings and so are still not readily available for automated analysis. This repo seeks to provide these PDF documents for distribution and convert these PDFs into UTF-8 documents for easier analysis.

Both the source PDFs and the generated UTF-8 are free to distribute.

## source 
The source folder provides the Quran narrarations and readings collected in their received PDF form.

## intermediate
The intermediate folder provides generated data from intermediate steps that can be useful for process analysis and verification as well as populating databases and further analysis with future tools. The data format is typically JSON.

## generated 
The generated folder provides the resulting UTF-8 texts for each Quran. These will be in TXT files.

## bin
The script performing the parsing and generation

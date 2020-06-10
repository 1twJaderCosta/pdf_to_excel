
# import tika
# import pandas as pd

# tika.initVM()
# from tika import parser
# parsed = parser.from_file('./file1.pdf')
# #print(parsed["metadata"])

# data  = parsed["content"]
# df = pd.read_csv(data)
# print(df)



##################################
### Import Libraries
##################################
import pandas as pd
import pytesseract
import subprocess
import os
import re

from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from PIL import Image
from tika import parser
from shutil import copyfile
from unidecode import unidecode

##################################
### Definitions
##################################
pdf_folder = '1.PDFs'                  # PDFs folder name
renamed_pdf_folder = '2.RENAMED_PDFs'  # Unidecoded rename pdf folder
TIKA_txt_folder = '3.TXT_TIKA'         # TIKA Text files folder name
TIKA_excel_folder = '4.EXCEL_TIKA'     # TIKA Excel files folder name


##################################
### Functions
##################################

def TIKA_convertPDF(file):

    meta = parser.from_file(file, 'http://localhost:9998/tika')

    # Check if parsed content is NoneType and handle accordingly.
    if "content" in meta and meta['content'] is None:

            # Run ImageMagick via subprocess (command line)
            params = ['convert', '-density', '300', '-depth', '8', '-strip',
                      '-background', 'white', '-alpha', 'off', 'temp.tiff']
            subprocess.check_call(params)

            # Run Tika again on new temp.tiff file
            meta = parser.from_file('temp.tiff', 'http://localhost:9998/tika')

            # Delete the temporary file
            os.remove('temp.tiff')

    return meta['content']


##################################
### Main Program
##################################

if __name__ ==  '__main__':

    ## Folders Logics
    if not(os.path.isdir(pdf_folder)):
        print("PDFs folder does not exist. Please, create the PDF folder and fill it with files before proceed.")

    if not(os.path.isdir(renamed_pdf_folder)):
        os.mkdir(renamed_pdf_folder)

    if not(os.path.isdir(TIKA_txt_folder)):
        os.mkdir(TIKA_txt_folder)

    if not(os.path.isdir(TIKA_excel_folder)):
        os.mkdir(TIKA_excel_folder)


    ## Reading and processing PDF files
    document_number = 1
    document_names = []

    for pdf_file in os.listdir('./' + pdf_folder):

        print('Reading PDF file: ' + pdf_file + ' ...')

        # Document number control
        document_names.append([document_number, pdf_file])

        pdf_orig_number = '000' + str(document_number)
        pdf_orig_number = pdf_orig_number[-3:]

        # Copy and Rename file using unidecode
        src = './' + pdf_folder + '/' + pdf_file

        pdf_file = 'PDF_' + pdf_orig_number + '.pdf'
        pdf_path = os.path.join(renamed_pdf_folder, pdf_file)

        copyfile(src, pdf_path)

        print('-----')

        try:
            # Read file and split lines and spaces - USING TIKA
            file_cont = TIKA_convertPDF(pdf_path)

            file_cont = file_cont.replace('-\n', '')
            file_cont = file_cont.replace('\n\n','|')
            file_cont = file_cont.replace('\n',' ')

            split_file_cont = file_cont.split("|")

            # Save file as TXT
            txt_file_name = 'TXT_PDF' + pdf_orig_number + '.txt'
            txt_file = open(os.path.join(TIKA_txt_folder, txt_file_name),
                            "w+", encoding = "utf-8")

            for line in split_file_cont:
                txt_file.write(line)
            txt_file.close()

            # Save file as EXCEL
            df_split_file_cont = pd.DataFrame(split_file_cont)
            excel_file_name = 'DF_TIKA_PDF' + pdf_orig_number + '.xlsx'
            df_split_file_cont.to_excel(os.path.join(TIKA_excel_folder, excel_file_name))

        except:
            print('ERROR WHILE USING TIKA TO CONVERT: ' + document_names[-1][1])

        document_number += 1

    document_names = pd.DataFrame(document_names, columns = ['PDF_NUMBER', 'PDF_ORIG_NAME'])
    document_names.to_excel('REF_TABLE.xlsx')

    print('---------------------------------------')
    print('PDF conversion process COMPLETE!')
    print('---------------------------------------')











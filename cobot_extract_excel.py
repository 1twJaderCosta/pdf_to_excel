import pandas as pd
import re

df = pd.read_excel('./4.EXCEL_TIKA/DF_TIKA_PDF003.xlsx')

patternOrder1 = "[0-9]+ 0   OP"
number = ''

patternOrder2 = "SUB-TOTAL:"
patternOrder3 = ",0 EA "
init = 0
header = []
itens = []

quantity = 0
catalog_number = ''
unit_price = 0
requested_date = ''
line = 0

for index, row in df.iterrows():
    if(len(str(row.iloc[1])) > 5):

        line = str(row.iloc[1])
        #print(line)

        match1 = re.match(patternOrder1, line)
        if(match1):
            number = line.split(' 0   OP')[0]

        match2 = re.match(patternOrder2, line)
        if(init == 1):
            if(line.find(patternOrder3)!= -1):
                header.append(line)
            else:
                itens.append(line)

        if(match2):
            init = 1

for count in range(0, len(header)):
    hd = header[count].split(' ')
    line = count
    sl = slice(0,8)  
    if(hd[2] == 'EA'):
        quantity = hd[1].split(',')[0]
        catalog_number = hd[0]
        unit_price = hd[3]
        requested_date = hd[5][sl]   
    else:
        quantity = hd[0].split(',')[0]
        unit_price = hd[2]
        equested_data = hd[4][sl]  


    it = itens[count]

    print(line)
    print(quantity)
    print(catalog_number)
    print(unit_price)
    print(requested_date)
    print(quantity)
    print(it)
    print('--------------------------------------')

print(number)
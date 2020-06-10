import pandas as pd
import re

df = pd.read_excel('./4.EXCEL_TIKA/DF_TIKA_PDF001.xlsx')

patternOrderDate = "Número : [0-9]+ Fecha : [0-9]+"
number = ''
date = ''

patternOrder1 = "Item Codigo Descripción Cant UM P"
patternOrder2 = "La Papelera del Plata S.A. Otto Krause 4950,"
patternOrder3 = "Valor neto total USD"
init = 0
itens = []
orderList = ''

for index, row in df.iterrows():
    if(len(str(row.iloc[1])) > 5):

        line = str(row.iloc[1])
        #Number and Date
        result = re.match(patternOrderDate, str(row.iloc[1]))
        if(result):
            splitone = line.split(' Comprador :')
            splittwo = splitone[0].split('Fecha : ')
            splitthree = splittwo[0].split('Número : ')
            number = splitthree[1]
            date = splittwo[1]

        #Order
        if(line.find(patternOrder1) != -1):
            init = 1
        if(line.find(patternOrder2) != -1):
            init = 0
        if(line.find(patternOrder3) != -1):
            init = 0
        if(init == 1):
            if(line.find("Item Codigo Descripción Cant") == -1 and line.find("_________________________________________________") == -1):
                itens.append(line)

#order continue
for it in itens:
    if(len(it) > 80):
        #print(it.split("      ")[0])
        orderList += '||'+it
    else: 
        orderList += ';'+it


# print(number)
# print(date)
#print(orderList)

# teste = orderList.split("||")[1]
# print(teste)

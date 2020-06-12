import re
import parse
import pdfplumber
import pandas as pd
from collections import namedtuple

Line = namedtuple('Line', 'Company_Name Invoice_No Invoice_Date Item_Details Quantity Unit_Price Gross_Ex_GST GST Gross_Inc_GST')
invoice_re = re.compile(r'Invoice No')
date_re = re.compile(r'\d{2}/\d{2}/\d{4}')
line_re = re.compile(r'(\$\w+.\w+ \$\w+.\w+)') 

#file = input("What is the FileName:  ")
file = 'Input/Invoice.pdf'
lines = []

company_name = "FRESH JASMINES PTY LTD"
with pdfplumber.open(file) as pdf:
    pages = pdf.pages
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):

            if invoice_re.search(line):
              inv_no = line.split()
              #print(inv_no[2])
            elif date_re.search(line):
                inv_dt = line.split()
                #print(inv_dt[2])
            elif line_re.search(line):
                item_line = line.split('$')
                GROSS_AMOUNT_IGST = item_line[-1]
                GST_AMT = item_line[-2]
                GROSS_AMOUNT_EGST = item_line[-3]
                UNIT_PRC = item_line[-4]
                QTY_line = item_line[0].rsplit(None,1)
                QTY = QTY_line[1]
                item = QTY_line[0]
                lines.append(Line(company_name, inv_no[2], inv_dt[2], item, QTY, UNIT_PRC, GROSS_AMOUNT_EGST, GST_AMT, GROSS_AMOUNT_IGST))

df = pd.DataFrame(lines)
df.head()
df['Invoice_Date'] = pd.to_datetime(df['Invoice_Date'])

out = file.split('.',1)[0]
out = out.split('/',1)[1]
fext = 'xls'
outfile = "Output/%s.%s" %(out,fext)

df.to_csv(outfile,index=False)
print("PDF is converted to Text file and saved in " + outfile)
print("=========================================================")
with open(outfile) as f:
    read_data = f.read()
    print(read_data)
    f.close()

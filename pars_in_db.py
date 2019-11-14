from openpyxl import load_workbook
import time
import progressbar
from main import app
from models import db, MainPrice, Competitor
import os
import xlrd





def loadAndUpdate(path,file_name):
    fullpath = os.path.join(path, file_name)
    base=os.path.basename(fullpath)
    wb = xlrd.open_workbook(fullpath)

    file_name = os.path.splitext(base)[0]
	
    sheet = wb.sheet_by_index(0)	
    max_rows = sheet.nrows	

    col_a = 0 #column 'C'
    col_b = 1 #column 'F'
    
    
    if file_name == 'AppleHelp.ru':
        for index in range(max_rows):
            row = sheet.row_values(index)
            name = row[col_a]
            price = row[col_b]
            try:
                record = MainPrice.query.filter_by(name=name).first()
                if record is not None:
                    rows = MainPrice.query.filter_by(name=name).update({'low_price': float(price)})
                else:	
                    if (name != None) and (price not in (None, 'ОПТ 3', 'Цена', 'Грин', 'Дилер', ' ', '')): 
                        rows = MainPrice(name=name, 
								low_price=float(price))
                        db.session.add(rows)
                db.session.commit()
            except:
                db.session.rollback()
        

    else:
        for index in range(max_rows):
            row = sheet.row_values(index)
            name = row[col_a]
            price = row[col_b]
            try:		
                record = Competitor.query.filter_by(comp_name=file_name,name=name).first()
                if record is not None:
                    rows = Competitor.query.filter_by(name = name).update({'low_price': float(price)})
                else:	
                    if (name != None) and (price not in (None, 'ОПТ 3', 'Цена', 'Грин', 'Дилер', ' ', '')): 
                        rows = Competitor(comp_name=file_name, name=name, 
						    	low_price=float(price))
                        db.session.add(rows)
                db.session.commit()
            except:
                db.session.rollback()

		
		
#        if (name != None) and (price not in (None, 'Цена', 'Грин', 'Дилер', ' ', '')): 
#            record = MainPrice(name=name, 
#								low_price=float(price))
#            db.session.add(record)
#            db.session.commit()
    return ''

def readDici():
#Парсинг прайса Диси
	
    wb = xlrd.open_workbook(filename = './data/dici.xlsx')

    for sheet_num in range(0, 5):
        sheet = wb.sheet_by_index(sheet_num)
	
        max_rows = sheet.nrows

        col_a = 0 #column 'A'
        col_b = 1 #column 'B'
        col_d = 3 #column 'D'
        col_e = 4 #column 'E'
	
        bar = progressbar.ProgressBar(maxval=max_rows, widgets=[
        progressbar.Bar(left='Dici Progress: [', marker='*', right=']')]).start()			
	
        for index in range(max_rows):
        
            row = sheet.row_values(index)
            if sheet_num == 0:
                name = row[col_a] + row[col_b]
                price = row[col_e]
            else:
                name = row[col_a]
                price = row[col_d]

			

            if (name != None) and (price not in (None, 'ОПТ 3', 'Цена', 'Грин', 'Дилер', ' ', '')): 

                record = Competitor(comp_name='Dici', name=name, 
								low_price=float(price))
                db.session.add(record)
                db.session.commit()
        bar.update(index)
    bar.finish() 	

				
def readGreens():
    wb = xlrd.open_workbook(filename = './data/greenspark.xlsx')
    sheet = wb.sheet_by_index(0)
	
    max_rows = sheet.nrows

    col_a = 0 #column 'A'
    col_p = 15 #column 'P'
	
    bar = progressbar.ProgressBar(maxval=max_rows, widgets=[
    progressbar.Bar(left='Green Progress: [', marker='*', right=']')]).start()			
	
    for index in range(max_rows):
        
        row = sheet.row_values(index)
        name = row[col_a]
        price = row[col_p]
        if (name != None) and (price not in (None, 'Цена', 'Грин', 'Дилер', ' ', '')): 

            record = Competitor(comp_name='GreenSpark', name=name, 
								low_price=float(price))
            db.session.add(record)
            db.session.commit()
        bar.update(index)
    bar.finish() 
				
			

def readAppleHelp():

    wb = xlrd.open_workbook(filename = './data/Прайс-лист AppleHelp.ru 06.05.xlsx')
    sheet = wb.sheet_by_index(0)
	
    max_rows = sheet.nrows

    col_c = 2 #column 'C'
    col_f = 5 #column 'F'
	
    bar = progressbar.ProgressBar(maxval=max_rows, widgets=[
    progressbar.Bar(left='AppleHelp Progress: [', marker='*', right=']')]).start()			
	
    for index in range(max_rows):
        
        row = sheet.row_values(index)
        name = row[col_c]
        price = row[col_f]
        if (name != None) and (price not in (None, 'Цена', 'Грин', 'Дилер', ' ', '')): 
            record = MainPrice(name=name, 
								low_price=float(price))
            db.session.add(record)
            db.session.commit()
        bar.update(index)
    bar.finish()    
	
		
	
	
def readNovena():
    wb = xlrd.open_workbook(filename = './data/novena.xls')
    sheet = wb.sheet_by_index(0)
	
    max_rows = sheet.nrows

    col_b = 1 #column 'B'
    col_g = 6 #column 'G'
	
    bar = progressbar.ProgressBar(maxval=max_rows, widgets=[
    progressbar.Bar(left='novena Progress: [', marker='*', right=']')]).start()			
	
    for index in range(max_rows):
        
        row = sheet.row_values(index)
        name = row[col_b]
        price = row[col_g]
        if (name != None) and (price not in (None, 'Цена', 'Цена3', 'Грин', 'Дилер', ' ', '')): 

            record = Competitor(comp_name='Novena', name=name, 
								low_price=float(price))
            db.session.add(record)
            db.session.commit()
        bar.update(index)
    bar.finish() 	

def main():

    loadAndUpdate('/data/','Dici')
#    readNovena()
#    readAppleHelp()
#    readDici()	 
#    readGreens()	 
	 
if __name__ == '__main__':
    main()

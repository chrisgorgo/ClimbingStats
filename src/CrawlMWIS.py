'''
Created on 22 Nov 2010

@author: filo
'''
from scrappers import MWIS
import os
from config import db_file
import sqlite3
if __name__ == '__main__':
    
    areas = ['nw', 'wh', 'eh', 'sh', 'su', 'ld', 'sd', 'pd']
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for area in areas:
        mwis = MWIS(area)
        mwis.scrap()
        
        mwis.save(c)
        
    conn.commit()
    conn.close()
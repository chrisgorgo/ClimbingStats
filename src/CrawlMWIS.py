'''
Created on 22 Nov 2010

@author: filo
'''
from scrappers import MWIS
import os
from config import db_file
if __name__ == '__main__':
    
    areas = ['nw', 'wh', 'eh', 'sh', 'su', 'ld', 'sd', 'pd']
    
    for area in areas:
        print area
        mwis = MWIS(area)
        mwis.scrap()
        mwis.save(db_file)
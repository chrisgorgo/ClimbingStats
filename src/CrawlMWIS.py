'''
Created on 22 Nov 2010

@author: filo
'''
from scrappers import MWIS
import os
if __name__ == '__main__':
    
    areas = ['nw', 'wh', 'eh', 'sh', 'su', 'ld', 'sd', 'pd']
    
    for area in areas:
        print area
        mwis = MWIS(area)
        mwis.scrap()
        mwis.save(os.path.abspath("ukc.db"))
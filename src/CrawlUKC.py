'''
Created on 21 Nov 2010

@author: Filo
'''
from scrappers import Crag
import os
from config import db_file
import sqlite3

if __name__ == '__main__':
    from generate_report import reports_dict
    crags_to_crawl = []
    for crags in reports_dict.values():
        crags_to_crawl += crags
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for crag_id in crags_to_crawl:
        scrapper = Crag(id=crag_id)
        new_jobs = scrapper.scrap()
        scrapper.save(c)
        
        for job in new_jobs:
            job.scrap()
            job.save(c)
        
    conn.commit()
    conn.close()
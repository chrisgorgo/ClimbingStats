'''
Created on 21 Nov 2010

@author: Filo
'''
from scrappers import Crag
import os

if __name__ == '__main__':
    from generate_report import reports_dict
    crags_to_crawl = []
    for crags in reports_dict.values():
        crags_to_crawl += crags
    
    for crag_id in crags_to_crawl:
        scrapper = Crag(id=crag_id)
        new_jobs = scrapper.scrap()
        print scrapper.name
        print scrapper.routes_ids
        scrapper.save(os.path.abspath("~/Dropbox/Public/ClimbingStats/ukc.db"))
        
        for job in new_jobs:
            job.scrap()
            job.save(os.path.abspath("~/Dropbox/Public/ClimbingStats/ukc.db"))
        
        
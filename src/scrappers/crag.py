'''
Created on 21 Nov 2010

@author: Filo
'''
import urllib2
from lxml import etree
from StringIO import StringIO
import sqlite3
from route import Route

class Crag(object):
    '''
    classdocs
    '''


    def __init__(self, id):
        '''
        Constructor
        '''
        self.id = id
        
    def scrap(self):
        filehandle = urllib2.urlopen('http://www.ukclimbing.com/logbook/crag.php?id=%d'%self.id)
        content = filehandle.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)
        
        self.name = tree.xpath(".//h1")[0].text
        self.routes_ids = [int(route_el.get("href")[8:]) for route_el in tree.xpath("//td/a[starts-with(@href, 'c.php')]")]
        return [Route(id, self.id) for id in self.routes_ids]
    
    def save(self, file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO crags (id, name) VALUES (?,?)", (self.id, self.name))
        conn.commit()
        conn.close()
        
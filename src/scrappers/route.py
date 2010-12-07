'''
Created on 21 Nov 2010

@author: Filo
'''
import urllib2, re
from lxml import etree
from StringIO import StringIO
from datetime import datetime

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data).strip()

def find_date(string):
    p = re.compile("\d\d/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d\d")
    date_str = p.search(string)
    if date_str == None:
        return date_str
    return datetime.strptime(date_str.group(), "%d/%b/%y").date()

class Route(object):
    '''
    classdocs
    '''


    def __init__(self, id, crag_id):
        '''
        Constructor
        '''
        self.id = id
        self.crag_id = crag_id
        
    def scrap(self):
        filehandle = urllib2.urlopen('http://www.ukclimbing.com/logbook/c.php?i=%d'%self.id)
        content = filehandle.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)
        
        self.name = tree.xpath(".//font[@size=5]/b")[0].text
        grade_node = tree.xpath(".//td[@align='right']/b")[0]
        grade_split = etree.tostring(grade_node, method="text").strip().split()
        self.grade1 = grade_split[0]
        if len(grade_split) == 2:
            self.grade2 = grade_split[1]
        else:
            self.grade2 = None
        
        
        log_entries = tree.xpath(".//table[@cellpadding='5']")[0]
        log_entries_text = etree.tostring(log_entries)
        self.log_entries = []
        if log_entries_text.find("<i>This climb isn't in any logbooks") != -1:
            self.log_entries = []
        else:
            self.log_entries = []
            cur_com = None
            cur_date = ""
            log_entries_text = re.sub("This climb is in \d+ logbook[s]*, and on .* wishlist[s]*.", "", log_entries_text)
            log_entries_text = log_entries_text.replace("PUBLIC&#160;LOGBOOKS","")
            for bit in log_entries_text.split("<br />"):
                if bit.startswith("<img src="):
                    cur_com = None
                    cur_date = ""
                    continue
                elif bit.find('<font color="#666666"') != -1:
                        cur_date = find_date(bit)
                        self.log_entries.append((cur_com, cur_date))
                        cur_com = None
                        cur_date = ""
                elif bit.find('Users with this climb on their wishlist are') != -1:
                    break
                else:
                    cur_com = remove_html_tags(bit)
        filehandle.close()
    
    def save(self, c):
        c.execute("INSERT OR REPLACE INTO routes (id, name, grade1, grade2, crag_id) VALUES (?,?,?,?,?)", (self.id, self.name, self.grade1, self.grade2, self.crag_id))
        c.execute("DELETE FROM logs WHERE route_id = ?", (self.id,))
        for log in self.log_entries:
            c.execute("INSERT OR REPLACE INTO logs (date, comment, route_id) VALUES (?,?,?)", (log[1], log[0], self.id))
        
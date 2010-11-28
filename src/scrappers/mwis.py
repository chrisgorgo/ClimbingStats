import urllib2
from lxml import etree
from StringIO import StringIO
from datetime import datetime


class MWIS(object):
    '''
    classdocs
    '''


    def __init__(self, id):
        '''
        Constructor
        '''
        self.id = id
        
    def scrap(self):
        filehandle = urllib2.urlopen('http://www.mwis.org.uk/%s.php'%self.id)
        content = filehandle.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)
        
        nodes = tree.xpath(".//div[@id='text']/*")
        i = 0
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("Viewing forecast for ") and node.tag == "h5":
                self.date = datetime.strptime(node.text[len("Viewing forecast for "):].replace("st","").replace("nd","").replace("rd","").replace("th", "").replace("Suay","Sunday").replace("Satuay", "Saturday"), "%A, %d %B, %Y")
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("Headline") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.headline = node.text
                break
        
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("How Windy?") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.how_windy = node.text
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("Effect Of Wind?") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.effect_of_wind = node.text
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("How Wet?") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.how_wet = node.text
                break
        
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("Cloud on the hills?") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.cloud_on_the_hills = node.text
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("Chance of cloud free") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.cloud_free_munros = node.text
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and node.text.startswith("Sunshine and air clarity?") and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.clarity = node.text
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and (node.text.startswith("How Cold") or node.text.startswith("Temperature")) and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.how_cold = node.text
                break
            
        while i < len(nodes):
            node = nodes[i]
            i+=1
            if node.text and (node.text.startswith("Freezing level") or node.text.startswith("And in the valleys")) and node.tag == "h5":
                node = nodes[i]
                i+=1
                self.freezing_level = node.text
                break
        filehandle.close()
        
    def save(self,c):
        c.execute("""INSERT OR REPLACE INTO forecasts 
        (area_id, date, headline, how_windy, effect_of_wind, how_wet, cloud_on_the_hills, cloud_free_munros, clarity, how_cold, freezing_level) 
        VALUES (?,?,?, ?,?,?, ?,?,?, ?, ?)""", (self.id, self.date, self.headline, self.how_windy, self.effect_of_wind, self.how_wet, self.cloud_on_the_hills, self.cloud_free_munros, self.clarity, self.how_cold, self.freezing_level))
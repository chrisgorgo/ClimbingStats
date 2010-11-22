'''
Created on 21 Nov 2010

@author: Filo
'''
import re
from datetime import date, datetime
test_str = 'Hidden - 2nd O/S - 09/May/08'

p = re.compile("\d\d/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d\d")
print datetime.strptime(p.search(test_str).group(), "%d/%b/%y").date()
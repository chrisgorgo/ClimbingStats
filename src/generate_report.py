'''
Created on 21 Nov 2010

@author: Filo
'''
import os
import sqlite3

def get_logs(crags):
    conn = sqlite3.connect(os.path.abspath("ukc.db"))
    c = conn.cursor()
    c.execute("""SELECT l.date as date, l.comment as comment , r.name as route_name, r.id, c.name as crag_name,  c.id, r.grade1, r.grade2
FROM logs l,
routes r, crags c
WHERE
    l.date > date('now','-7 days')
    AND l.route_id = r.id
    AND r.crag_id = c.id
    AND c.id in ( %s )
    ORDER BY l.date   DESC""" % (",".join([str(crag) for crag in crags])))
    conn.commit()
    rows = c.fetchall()
    conn.close()
    return rows

reports_dict = {"Cairngorms": [25, 74, 28, 3614, 3613, 32, 305, 2520],
                "Ben Nevis": [648, 808, 645, 644, 643, 807, 641, 642, 646, 647,808, 809, 649, 10615, 10616, 3761, 9375, 650],
                "Peak District": [1341, 134, 1239, 1225, 9849, 1335, 120, 148, 108, 2624, 11145]}

if __name__ == '__main__':
    f = open('report.html', 'w')
    f.write("<h1>Last 7 days of climbing in...</h1>")

    for name, crags in reports_dict.iteritems():
        f.write("""<h2>%s</h2><table><tr>
    <th>date</th>
    <th>comment</th>
    <th>route_name</th>
    <th>crag_name</th></tr>"""%name)
        rows = get_logs(crags)
        for row in rows:
            f.write("<tr>")
            f.write("<td>%s</td>"%row[0])
            f.write("<td>%s</td>"%(row[1]))
            if row[7] != None:
                grade = row[6] + " " + row[7]
            elif row[6] != None:
                grade = row[6]
            else: 
                grade = ""
            f.write("<td><a href='http://www.ukclimbing.com/logbook/c.php?i=%d'>%s %s</a></td>"%( row[3], row[2], grade))
            f.write("<td><a href=http://www.ukclimbing.com/logbook/crag.php?id=%d'>%s</a></td>"%(row[5],row[4]))
            f.write("</tr>")
        f.write("</table>")
        
    f.write("""<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-339450-6']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>""")
        
    f.close()
            
            
    
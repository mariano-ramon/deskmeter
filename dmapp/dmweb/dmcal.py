import datetime
from pprint import pprint
from flask import Blueprint, render_template
import pytz

import calendar


from dmweb.dm import dmbp, get_period_totals, local_date



class DMHTMLCalendar(calendar.HTMLCalendar):


    # def formatmonth(self, theyear, themonth, withyear=True):
    #     self.dmmonth = themonth
    #     super().formatmonth(self, theyear, themonth)


    def setcalmonth(self, month):
        self.dmmonth = month

    def oneday(self,month,day):

        start = datetime.datetime(2020, month, day).replace(hour=0,
                                                  minute=0,
                                                  second=0)

        end = datetime.datetime(2020, month, day).replace (hour=23,
                                                 minute=59,
                                                 second=59)

        rows = get_period_totals( local_date(start), 
                                  local_date(end))

        returnstr = "<table class='totaltable'>"
        for row in rows:
            returnstr += "<tr><td>{}</td><td>{}</td></tr>".format(row["ws"],row["total"])

        returnstr += "</table>"
        return returnstr 


    def formatday(self, day, weekday):
            """
            Return a day as a table cell.
            """
            if day == 0:
                return '<td class="noday">&nbsp;</td>' # day outside month
            else:
                return '<td class="%s">%s</td>' % (self.cssclasses[weekday], self.oneday(self.dmmonth, day))



@dmbp.route("/calendar")
@dmbp.route("/calendar/<int:month>")
def calmain(month=None):

    usemonth = datetime.datetime.today().month
    if month:
        usemonth = month
    
    cal = DMHTMLCalendar(calendar.SATURDAY)

    cal.setcalmonth(usemonth)
        
    return render_template("calendar.html", content=cal.formatmonth(2020,usemonth))


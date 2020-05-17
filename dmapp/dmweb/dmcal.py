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


    def oneweek(self,month,week):

        start_day = None
        end_day = None

        for (d, wd) in week:
            if d == 0:
                continue
            else:
                start_day = d
                break


        for (d, wd) in reversed(week):
            if d == 0:
                continue
            else:
                end_day = d
                break


        start = datetime.datetime(2020, month, start_day).replace(hour=0,
                                                  minute=0,
                                                  second=0)

        end = datetime.datetime(2020, month, end_day).replace (hour=23,
                                                 minute=59,
                                                 second=59)

        rows = get_period_totals( local_date(start), 
                                  local_date(end))

        returnstr = "<table class='totaltable'>"
        for row in rows:
            returnstr += "<tr><td>{}</td><td>{}</td></tr>".format(row["ws"],row["total"])

        returnstr += "</table>"
        return returnstr 


    # def formatmonthname(self, theyear, themonth, withyear=True):
    #     """
    #     Return a month name as a table row.
    #     """
    #     if withyear:
    #         s = '%s %s' % (month_name[themonth], theyear)
    #     else:
    #         s = '%s' % month_name[themonth]
    #     return '<tr><th colspan="8" class="%s">%s</th></tr>' % (
    #         self.cssclass_month_head, s)


    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        s += "<td>Week Totals</td>"
        return '<tr>%s</tr>' % s



    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        s += "<td>{}</td>".format(self.oneweek(self.dmmonth, theweek))
        return '<tr>%s</tr>' % s


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


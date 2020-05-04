from collections import Counter
import datetime
from pprint import pprint

from flask import Blueprint, render_template
from pymongo import MongoClient
import pytz

client = MongoClient()
db = client.deskmeter
switches = db.switch

dmbp = Blueprint("deskmeter", __name__, url_prefix="/", template_folder='templates')

@dmbp.route("/")
def index():
    """
        Show total time used in each desktop for today
    """

    start = datetime.datetime.today().replace(hour=0, 
                                              minute=0, 
                                              second=0)

    end = datetime.datetime.today().replace (hour=23, 
                                             minute=59, 
                                             second=59)

    rows = get_period_totals( local_date(start), 
                              local_date(end))

    return render_template("pages.html", rows=rows)


@dmbp.route("/day/<int:month>/<int:day>")
def oneday(month,day):

    start = datetime.datetime(2020, month, day).replace(hour=0,
                                              minute=0,
                                              second=0)

    end = datetime.datetime(2020, month, day).replace (hour=23,
                                             minute=59,
                                             second=59)

    rows = get_period_totals( local_date(start), 
                              local_date(end))

    return render_template("pages.html", rows=rows)



@dmbp.route("/period/<start>/<end>")
def period(start,end):

    start = datetime.datetime(*map(int, start.split("-"))).replace(hour=0,
                                              minute=0,
                                              second=0)

    end = datetime.datetime(*map(int, end.split("-"))).replace (hour=23,
                                             minute=59,
                                             second=59)

    rows = get_period_totals( local_date(start), 
                              local_date(end))

    return render_template("pages.html", rows=rows)


@dmbp.route("/totals")
def totals():
    """
        Show total time used in each desktop for all time
    """

    pipe =  [{'$group': {'_id':"$workspace",'totals': {'$sum': '$delta'}}},
             {'$sort':  { "_id": 1}}]

    rows = []    
    for total in switches.aggregate(pipeline=pipe):
        rows.append( {"ws"   : total["_id"], 
                      "total": str(datetime.timedelta(seconds=total["totals"]))})

    
    return render_template("pages.html", rows=rows)


def get_period_totals(start, end):
    """
    TODOs: refactor to have available the ws array and the active ws function in order to remove
    the delta = 0 thing
    refactor to pass in the timezone and make the variable names clearer
    """

    queries = {
        "period" : {"date": {"$gt" : start, "$lt" : end }},
        "previous_doc" : {"date" : {"$lt" : start }}
        #"next_doc" : {"date":{"$lt":start}}
    }

    length = switches.count_documents(queries["period"])
    docs =  switches.find(queries["period"]).sort([("date", 1)])
    
    if not length:
        return [{"ws": "No Data", "total": ""}]
    #next_doc = switches.find_one(queries["next_doc"])
    last_doc = docs[length-1]

    first_date = local_date(docs[0]["date"], True)
    last_date = local_date(last_doc["date"], True)

    pipe =  [   {'$match': queries["period"] },
                {'$group': { '_id':"$workspace",'totals': {'$sum': '$delta'}}},
                {'$sort':  { "_id": 1}}]

    pre_rows = Counter({})
    for total in switches.aggregate(pipeline=pipe):
        pre_rows[total["_id"]] = total["totals"]

    time_corrections = []
    if first_date > start:
        #TODO if its the first record it fails write test
        try:
            previous_doc = switches.find(queries["previous_doc"]).sort([("date", -1)]).limit(1)[0]
            time_corrections.append(Counter({previous_doc["workspace"] : split_entry(previous_doc, start)}))
        except IndexError:
            pass
        
        
    
    now = local_date(datetime.datetime.now())

    if end > now:
        time_corrections.append(Counter({ last_doc["workspace"] : split_entry(last_doc, now, after=False)}))

    if end > last_date and now > end:
        time_corrections.append(Counter({ last_doc["workspace"] : split_entry(last_doc, end, after=False)}))

    for correction in time_corrections:
        pre_rows += correction

    #TODO _1 remove
    #day = 0
    rows = []
    for ws, total in pre_rows.items():
        #TODO _1 remove
        #day += total
        rows.append( {"ws": ws,
                      "total" : datetime.timedelta(seconds=total)})

    #TODO _1 remove
    #rows.append({"ws":"sum","total": day})
    return rows


def split_entry(entry, split_time, after=True):
    """
        entry must have a date an number
        split_time must be timezone aware
        after bolean to return the time after the split time
    """
    first_half = round((split_time - local_date(entry["date"], True)).total_seconds())
    last_half = entry["delta"] - first_half
    if after:
        return last_half

    return last_half * -1


def local_date(date, convert=False):
    bsas = pytz.timezone("Etc/GMT+3")
    if convert:
        return pytz.utc.localize(date, is_dst=None).astimezone(bsas)
    return date.replace(tzinfo=bsas)

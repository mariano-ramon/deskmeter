from flask import Blueprint, render_template
from pymongo import MongoClient
from pprint import pprint
import datetime
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

    rows = get_period_totals(start, end)

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

  bsas = pytz.timezone("Etc/GMT+3")
  local_start = start.replace(tzinfo=bsas)
  local_end = end.replace(tzinfo=bsas)

  queries = {
      "period" : {"date":{"$gt":local_start,"$lt":local_end}},
      "previous_doc" : {"date":{"$lt":local_start}}
      #"next_doc" : {"date":{"$lt":local_start}}
  }

  length = switches.count_documents(queries["period"])
  docs =  switches.find(queries["period"]).sort([("date", 1)])
  previous_doc = switches.find_one(queries["previous_doc"])
  #next_doc = switches.find_one(queries["next_doc"])
  last_doc = docs[length-1]

  local_first_date = docs[0]["date"].replace(tzinfo=pytz.utc).astimezone(bsas)
  local_last_date = last_doc["date"].replace(tzinfo=pytz.utc).astimezone(bsas)

  delta_to_start = (local_first_date - local_start).total_seconds()
  delta_to_end = (local_end - local_last_date).total_seconds()


  pipe =  [   {'$match': queries["period"] },
              {'$group': { '_id':"$workspace",'totals': {'$sum': '$delta'}}},
              {'$sort':  { "_id": 1}}]

  pre_rows = {}
  for total in switches.aggregate(pipeline=pipe):
      pre_rows[total["_id"]] = total["totals"]


  if datetime.datetime.now().astimezone(bsas) < local_end:
      delta_to_end = 0

  pre_rows[previous_doc["workspace"]] += round(delta_to_start)
  pre_rows[last_doc["workspace"]] += round(delta_to_end)

  rows = []
  for ws, delta in pre_rows.items():
      rows.append( {"ws": ws,
                    "total" : str(datetime.timedelta(seconds=delta))})

  return rows

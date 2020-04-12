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

    bsas = pytz.timezone("Etc/GMT-0")

    start = datetime.datetime.today().replace(hour=0, 
                                              minute=0, 
                                              second=0,
                                              tzinfo=bsas)


    end = datetime.datetime.today().replace (hour=23, 
                                             minute=59, 
                                             second=59,
                                             tzinfo=bsas)


    pipe =  [   {'$match': { 'date' : {"$gte": start, "$lt": end}} },
                {'$group': { '_id':"$workspace",'totals': {'$sum': '$delta'}}},
                {'$sort':  { "_id": 1}}]

    rows = []    
    for total in switches.aggregate(pipeline=pipe):
        rows.append( {"ws"   : total["_id"], 
                      "total": str(datetime.timedelta(seconds=total["totals"]))})


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

    print(rows)
    return render_template("pages.html", rows=rows)
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

    return pprint(rows)
    #return render_template("pages.html", rows=rows)








@dmbp.route("/totals")
def totals():
    """
        Show total time used in each desktop for all time
    """

    """
    split times on selected period
      cuantos segundos de diferencia desde el primer resultado al comienzo del periodo seleccionado
      
        TODO despues: calcular el delta del start al end y pedir recurrentemente esa franja para atras hasta que alguno de los registros supere la fecha/hora seleccionada
                      tambien puede ser ir incrementando el tamaño del bloque anterior a pedir hasta lograrlo
        
                cual es el ultimo registro del periodo anterior

        el delta es mayor a los segundos faltantes? 
          SI? PEOLA
          NO? Bu, bueno.
            LO VEMOS DESPUES caso edge de no registrado
      cuantos segundos faltan del final del periodo con el ultimo resultado
          ME CHUPA UN GUEVO (por ahora) siempre es el start del ultimo
          resultado hasta que termina el dia
    """








    pipe =  [{'$group': {'_id':"$workspace",'totals': {'$sum': '$delta'}}},
             {'$sort':  { "_id": 1}}]

    rows = []    
    for total in switches.aggregate(pipeline=pipe):
        rows.append( {"ws"   : total["_id"], 
                      "total": str(datetime.timedelta(seconds=total["totals"]))})

    
    return render_template("pages.html", rows=rows)


def get_period_totals(start,end):

    bsas = pytz.timezone("Etc/GMT-3")

    lstart = start.replace(tzinfo=bsas)
    lend = end.replace(tzinfo=bsas)

    pipe =  [   {'$match': { 'date' : {"$gte": start, "$lt": end}} },
                {'$group': { '_id':"$workspace",'totals': {'$sum': '$delta'}}},
                {'$sort':  { "_id": 1}}]

    rows = []    
    for total in switches.aggregate(pipeline=pipe):
        rows.append(total)

        # rows.append( {"ws"   : total["_id"], 
        #               "total": str(datetime.timedelta(seconds=total["totals"]))})

    return rows

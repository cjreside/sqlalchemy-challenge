# Imports
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 
import numpy as np 
import pandas as pd 

# Engine Creation
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflection
base = automap_base()
base.prepare(engine,reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = Base.classes.station

# Create our session from Python to the DB
session = Session(engine)

# Creating an App
app = Flask(__name__)

# Defining My Routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API Homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    # Return precipitation data for the last year
    first_day = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.station==most_active).filter(measurement.date>= first_day).all()

    p_dict={date: prcp for date, prcp in results}
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    stations = list(np.ravel(stations))
    return jsonify(stations) 

@app.route("/api/v1.0/tobs")
def temp(): 
    stations = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    most_active=stations[0][0]
    station_data = session.query(measurement.date, measurement.tobs).filter(measurement.station==most_active).all()
    station_data = list(np.ravel(station_data))
    return jsonify(station_data)


@app.route("/api/v1.0/<start>") 
def start(start):
    results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date>start).all()
    temps = list(np.ravel(results))
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date>=start).filter(measurement.date<=end).all()
    temps2 = list(np.ravel(results))
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

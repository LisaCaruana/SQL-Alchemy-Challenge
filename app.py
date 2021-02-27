import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
stations = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary using 
    # `date` as the key and `prcp` as the value.

    # Query precipitation data
    last_date=session.query(measurements.date).order_by(measurements.date.desc()).first()
    #print(last_date) #2017-8-23
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #print("Query Date: ", query_date)

# Perform a query to retrieve the data and precipitation scores
    yr_prcp= session.query(measurements.date, measurements.prcp).\
        filter(measurements.date > query_date).\
        order_by(measurements.date).all()

# Return the JSON representation of your dictionary.
    # Convert list of tuples into normal list
    prcp_dict=dict(yr_prcp)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station_names():
  # Perform a query to retrieve the stations list
    station_names= session.query(stations.name).all()
    
    # Convert list to json
    observatorys=list(np.ravel(station_names))
    return jsonify(observatorys)

@app.route("/api/v1.0/tobs")
def temp_observations():
  # Query the dates and temperature observations of the most active station for the last year of data.
    last_date=session.query(measurements.date).order_by(measurements.date.desc()).first()
    #print(last_date) #2017-8-23
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_data=[measurements.tobs]
    station_temp=session.query(*temp_data).filter(measurements.station=="USC00519281").filter(measurements.date>=query_date).all()
    
    # Convert list to json
    temp_list=list(np.ravel(station_temp))
    return jsonify(temp_list)

#  * Return a JSON list of the minimum temperature, the average temperature, 
#  and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, 
#   and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the
#    `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def beg_date(start):

    sel= [func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)]

    beg_results = session.query(*sel).\
        filter(measurements.date>=start).all()

    beg_temps = list(np.ravel(beg_results))
    return jsonify(beg_temps)
    
@app.route("/api/v1.0/<start>/<end>")  
def trip_date(start, end):

    sel2= [func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)]

    trip_results = session.query(*sel2).\
        filter(measurements.date>=start, measurements.date<=end).all()

    trip_temps = list(np.ravel(trip_results))
    return jsonify(trip_temps)

if __name__ == '__main__':
    app.run(debug=True)
    
#     results= session.query(*sel).\
#         filter(measurements.date>=start).\
#         filter(measurements.date<=end).all()

#         temps= list(np.ravel(results))
#         return jsonify(temps=temps)

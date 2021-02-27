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


# look up how to convert a list of tuples into a dictionary
# use for next one:   all_names = list(np.ravel(results)) np.ravel is for unraveling a list of tuples with one value in the tuples 
# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
# SQLAlchemy Project

This is a two-part project performs basic climate analysis and data exploration of a climate database. The analysis is completed using SQLAlchemy ORM queries, Pandas, and Matplotlib. The project was started by using a provided [starter notebook](climate_starter.ipynb) and [hawaii.sqlite](Resources/hawaii.sqlite) files to complete the climate analysis and data exploration.

## Part 1 - Initial Analysis

- A start date and end date for an imagined trip was chosen.

- SQLAlchemy `create_engine` was used to connect to the sqlite database.

- SQLAlchemy `automap_base()` was used to reflect the tables into classes, saving a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

- A query was designed to retrieve the last 12 months of precipitation data, selecting only the `date` and `prcp` values.

- The query results are loaded into a Pandas DataFrame and the index set to the date column.

- The DataFrame values are then sorted by `date`.

- The results are then plotted using the DataFrame `plot` method.

- Pandas is used to print the summary statistics for the precipitation data.

### Station Analysis

* A query was designed to calculate the total number of stations and the most active stations. 

  * Stations and observation counts are listed in descending order.

  * The station with the highest number of observations is noted.

* A query was designed to retrieve the last 12 months of temperature observation data (TOBS).

  * Stations were then filtered according to the highest number of observations.

  * The results are plotted as a histogram with `bins=12`.

- - -

## Part 2 - Climate App

A Flask API was designed based on the above queries, with Flask JSONIFY used to create JSON objects. Flask is used to create the following routes:

### Routes

* `/`

  * Home page.

  * Lists all routes that are available.

* `/api/v1.0/precipitation`

  * Converts the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Returns the JSON representation of this dictionary.

* `/api/v1.0/stations`

  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Querys the dates and temperature observations of the most active station for the last year of data.
  
  * Returns a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Returns a JSON list of the minimum temperature, average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculates the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
  
  
- - -
This assignment is from the University of Denver's Data Analytics Boot Camp. 
### Copyright

Trilogy Education Services © 2020. All Rights Reserved.


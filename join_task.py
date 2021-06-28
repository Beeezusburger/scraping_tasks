"""
Task1: Joins are best explained in single 9gag post: https://9gag.com/gag/an9yxbB

Task2:
    Add full airline name to the flights dataframe and show the arr_time, origin, dest and the name of the airline.
    SELECT flights.arr_time,
           flights.origin,
           flights.dest,
	       airlines.name
    FROM flights
    LEFT JOIN airlines ON flights.carrier=airlines.carrier;

    Filter resulting data.frame to include only flights containing the word JetBlue
    SELECT flights.arr_time,
           flights.origin,
           flights.dest,
	       airlines.name
    FROM flights
    LEFT JOIN airlines ON flights.carrier=airlines.carrier
    WHERE airlines.name='JetBlue Airways';

    Summarise the total number of flights by origin in ascending.
    SELECT origin, COUNT(origin)
    FROM flights
    GROUP BY origin
    ORDER BY origin ASC;

    Filter resulting data.frame to return only origins with more than 10,000 flights.
    SELECT origin, COUNT(origin)
    FROM flights
    GROUP BY origin
    HAVING COUNT(origin)>10000
    ORDER BY origin ASC;
"""
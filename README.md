# Using OpenTripPlanner (2.2.0) for querying origin-destination pairs for the mode of e-bike
One should have [osmosis](https://wiki.openstreetmap.org/wiki/Osmosis/Installation) installed 
to run some scripts in this repo.

## 1. Data preparation
Run `src/1-data-preparation.ipynb` to prepare data in the below table.
Specific methods can be found in `lib/dataworkers.py`.

| Step | Data                                                      |
|------|-----------------------------------------------------------|
| 1    | Prepare **GTFS data** and **DEM data** |
| 2    | Convert **boundary shapefile** to poly                       |
| 3    | Crop **country-level OSM** file with regional boundary (poly) |
| 4    | Build routable **OTP graph** with elevation and transit information                                |

Note: transit data is needed to run OTP e-bike routing because there is a bug in the current version of OTP. One can use a small set of GTFS data. 
However, having GTFS data included opens up more possibilities, e.g., "BICYCLE,TRANSIT".

More details can be found [here](https://docs.opentripplanner.org/en/dev-2.x/Basic-Tutorial/).

## 2. Routing with OTP's PlanAPI (in-memory server)
Run `src/otp-server-starter.py` to get the server started. And run `src/2-otp-routing.py` to get detailed itineraries of the OD pairs data
under `example/`.
Specific methods can be found in `lib/routing.py`.
With multiprocessing (implemented via `p_map` of the package p_tqdm), 1 million OD pairs cost around 2 hours*.

*Experiments were run on a computer with an Intel(R) Core(TM) i9-9900X CPU @ 3.50GHz
running at 2666 MHz using 64 GB RAM, on Windows 10.

## 3. Explore returned itineraries
Open `src/1-data-preparation.ipynb` to explore the results and get familiar with the API use.


TSP
===

CLI tool for calculating TSP optimal path given physical addresses.

"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the origin city?" - [Travelling_salesman_problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)


# Setup

  pip install -r requirements.txt

You also need to setup a [Google Maps Distance Matrix API key](https://developers.google.com/maps/documentation/distance-matrix/).


# Usage

  usage: tsp.py [-h] address_file api_key

  TSP for addresses.

  positional arguments:
    address_file  File with one address per line
    api_key       Google Maps Distance Matrix API key

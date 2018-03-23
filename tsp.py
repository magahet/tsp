'''tsp.py provides a cli tool for running tsp on a list of addresses.
The result is a cycle between addresses with the shortest travel duration.
'''

import argparse
import requests
import numpy as np
from tsp_solver.greedy import solve_tsp


def get_distances(address_list, key):
    '''Get distances from google maps api.'''
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    payload = {
        'origins': '|'.join(address_list),
        'destinations': '|'.join(address_list),
        'mode': 'driving',
        'api_key': key
    }

    response = requests.get(base_url, params=payload)
    return response.json()


def parse_distance_dict(dist):
    '''Translate the result from google api to distance matrix.'''
    matrix = np.zeros((len(dist['origin_addresses']),
                       len(dist['destination_addresses'])),
                      dtype=int)
    for isrc, _ in enumerate(dist['origin_addresses']):
        for idst, _ in enumerate(dist['destination_addresses']):
            row = dist['rows'][isrc]
            cell = row['elements'][idst]
            if cell['status'] == 'OK':
                matrix[isrc, idst] = cell['duration']['value']
    return matrix


def calc_duration(path, distance_matrix):
    '''Calculate the total duration to travel the cycle.'''
    total = 0
    for i in xrange(1, len(path)):
        total += distance_matrix[path[i-1]][path[i]]
    total += distance_matrix[path[-1]][path[0]]
    return total


def read_addresses(path):
    '''Read addresses from file.'''
    with open(path) as file_:
        return [l.strip() for l in file_.readlines()]


def main():
    '''Run tsp calc on address file.'''
    parser = argparse.ArgumentParser(description='TSP for addresses.')
    parser.add_argument('address_file', help='File with one address per line')
    parser.add_argument('api_key', help='Google Maps Distance Matrix API key')
    args = parser.parse_args()

    addresses = read_addresses(args.address_file)
    distances_dict = get_distances(addresses, args.api_key)
    distance_matrix = parse_distance_dict(distances_dict)
    path = solve_tsp(distance_matrix)

    print 'path:'
    for idx in path:
        print addresses[idx]
    print
    print 'cycle duration (sec):', calc_duration(path, distance_matrix)


if __name__ == '__main__':
    main()

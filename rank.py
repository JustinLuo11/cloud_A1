import json
from pprint import pprint
import time

start_time = time.time()

def get_melb_grid(filename):
    """
    Parse melbgrid.jsom file to a dictionary
    :param filename
    :return: []
    """

    grid = []

    with open(filename, 'r') as f:
        data = json.loads(f.read())
        for val in data["features"]:
            grid_dict = {}
            properties = val["properties"]
            grid_dict["id"] = properties["id"]
            grid_dict["xmax"] = properties["xmax"]
            grid_dict["xmin"] = properties["xmin"]
            grid_dict["ymin"] = properties["ymin"]
            grid_dict["ymax"] = properties["ymax"]
            grid.append(grid_dict)
        return grid

def get_sentiment_socres(data_path):
    """get the corresponding dict between sentiment and score"""
    with open(data_path) as f:
        lines = f.readlines()
    sentiment_scores = {}
    for line in lines:
        sentiment, score = line.strip().split('\t')
        sentiment_scores[sentiment] = int(score)
    return sentiment_scores

def get_cell(coordinate, grid):
    """get the cell name according to the location(x,y)"""
    for x_cell, x_range in grid['x'].items():
        if x_range[0] < coordinate[0] <= x_range[1]:
            x = x_cell
            break
    for y_cell, y_range in grid['y'].items():
        if y_range[0] < coordinate[1] <= y_range[1]:
            y = y_cell
            break
    return y+x

def process_twitter(twitter):
    if twitter.get('value'):
        if twitter['value'].get('coordinates'):


melb_grid = get_melb_grid('data/melbGrid.json')
word_value = get_sentiment_socres('data/AFINN.txt')
pprint(melb_grid)

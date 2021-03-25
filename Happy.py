import json
from nltk.tokenize import TweetTokenizer
class twitter_data:
    def __init__(self,json_data=None):
        self.json_data = json_data
        self.coordinates = None
        self.id = None
        self.text = None
        self.value = None
        self.geometry = None
        self.properties = None
        if self.json_data is not None:
            self.process_json_data()
    def process_json_data(self):
        self.id = self.json_data['id']
        self.value = self.json_data['value']
        if self.value is not None:
            self.geometry = self.value['geometry']
            if self.geometry is not None:
                self.coordinates = self.geometry['coordinates']
            self.properties = self.value['properties']
            if self.properties is not None:
                self.text = self.properties['text'].lower()
        return


#text

    #print(twitter.coordinates)


class Utility:
    def get_melb_grid(self):
        """
        Parse melbgrid.jsom file to a dictionary
        :param filename
        :return: []
        """
        grid = []
        with open('data/melbGrid.json', 'r') as f:
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

    def get_sentiment_socres(self):
        """get the corresponding dict between sentiment and score"""
        with open('data/AFINN.txt') as f:
            lines = f.readlines()
        sentiment_scores = {}
        for line in lines:
            sentiment, score = line.strip().split('\t')
            sentiment_scores[sentiment] = int(score)
        return sentiment_scores

    def get_cell(self, twitter, grid):
        cells = None
        for i in grid:
            if i['xmin'] < twitter.coordinates[0] <= i['xmax'] and i['ymin'] < twitter.coordinates[1] <= i['ymax']:
                cells = i['id']
        return cells

    def get_twitter_sentiment(self, twitter, score):
        tt = TweetTokenizer()
        sentiment = 0
        tweet = tt.tokenize(twitter.text)
        sentiment_score = 0
        for i in range(len(tweet)):
            if tweet[i] in score.keys():
                sentiment_score += score[tweet[i]]
        sentiment = sentiment_score
        return sentiment
    def get_cell_score(self, cells, sentiment):
        result = []
        result = [cells, sentiment]
        return result
    def get_results(self,grid):
        results = {}
        for i in grid:
            results[i['id']] = [0,0]
        return results


util = Utility()
grid = util.get_melb_grid()
score = util.get_sentiment_socres()
results = util.get_results(grid)
with open('data/tinyTwitter.json') as f:
    data = json.load(f)
for i in data['rows']:
    twitter = twitter_data(i)
    cells = util.get_cell(twitter,grid)
    sentiment = util.get_twitter_sentiment(twitter,score)
    cell_score = util.get_cell_score(cells,sentiment)

    for i in results.keys():
        if cell_score[0] == i:
            results[cell_score[0]][0] += 1
            results[cell_score[0]][1] += cell_score[1]
for i in results.items():
    print(i)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

response = requests.get("http://www.nytimes.com")
doc = BeautifulSoup(response.text, 'html.parser')

stories = doc.find_all("article", { 'class': 'story' })

all_stories = []
# Grab their headlines and bylines
for story in stories:
    # Grab all of the h2's inside of the story
    headline = story.find('h2', {'class': 'story-heading'})
    # If a headline exists, then process the rest!
    if headline:
        # They're COVERED in whitespace
        headline_text = headline.text.strip()
        # Make a dictionary with the headline
        this_story = { 'headline': headline_text }
        byline = story.find('p', {'class': 'byline'})
        # Not all of them have a byline
        if byline:
            byline_text = byline.text.strip()
            this_story['byline'] = byline_text
        all_stories.append(this_story)

all_stories

stories_df = pd.DataFrame(all_stories)
stories_df.to_csv("nyt-data.csv")

datestring = time.strftime("%Y-%m-%d-%H-%M")

filename = "nyt-data-" + datestring + ".csv"
stories_df.to_csv(filename, index=False)





https://api.darksky.net/forecast/13d3600a5cd0883a0f7c94181a175dd3/40.7128,-74.0059

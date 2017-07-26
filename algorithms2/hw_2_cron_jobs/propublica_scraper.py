import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

response = requests.get("https://www.propublica.org/")
doc = BeautifulSoup(response.text, 'html.parser')
stories = doc.find_all("div", { 'class': 'box-feature-text' })

all_stories = []
# Grab their headlines and bylines
for story in stories:
    # Grab all of the h2's inside of the story
    headline = story.find('a', {'class': 'title-link'})
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

print(all_stories)

stories_df = pd.DataFrame(all_stories)
stories_df.head()
stories_df.to_csv("propublica-data.csv")

datestring = time.strftime("%Y-%m-%d-%H-%M")

filename = "propublica-data-" + datestring + ".csv"
stories_df.to_csv(filename, index=False)

requests.post(
        "https://api.mailgun.net/v3/sandboxfde15846fe8f42e1ba424520b85f9de4.mailgun.org/messages",
        auth=("api", "key-b461543f82207a0b6573356521d9164d"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxfde15846fe8f42e1ba424520b85f9de4.mailgun.org>",
              "to": "Kate Cough <kc3053@columbia.edu>",
              "subject": "Propublica Headlines",
              "text": all_stories})
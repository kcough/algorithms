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
        #make a dictionary called 'this_story" inside your list 'all_stories'
        this_story = { 'headline': headline_text }
        #add a byline entry
        byline = story.find('p', {'class': 'byline'})
        #and one for links
        link = story.find('a', href=True)
        # Not all of them have a byline
        summary = story.find_all('p')
        if byline:
            byline_text = byline.text.strip()
            this_story['byline'] = byline_text
        #they should all have links but whatever
        if link:
            link_text = link.text.strip()
            this_story['link'] = link["href"]
        if len(summary) > 1:
            summary_text = summary[1].text
            this_story['summary'] = summary_text
            
        all_stories.append(this_story)

#flatten the dictionary into a string
text = ""

for story in all_stories: 
    text = text + story['headline'] + "\n"
    if 'byline' in story:
        text = text + story['byline'] + "\n"
    if 'summary' in story:
        text = text + story['summary'] + "\n"
    text = text + story['link'] + "\n"
    text = text + "\n\n"
text

# print(all_stories)

# stories_df = pd.DataFrame(all_stories)
# stories_df.head()
# stories_df.to_csv("propublica-data.csv")

# datestring = time.strftime("%Y-%m-%d-%H-%M")

# filename = "propublica-data-" + datestring + ".csv"
# stories_df.to_csv(filename, index=False)

requests.post(
        "https://api.mailgun.net/v3/sandboxfde15846fe8f42e1ba424520b85f9de4.mailgun.org/messages",
        auth=("api", "key-b461543f82207a0b6573356521d9164d"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxfde15846fe8f42e1ba424520b85f9de4.mailgun.org>",
              "to": "Kate Cough <kaitlin.cough@gmail.com>",
              "subject": "Propublica Headlines",
              "text": text})
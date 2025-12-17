
from pygooglenews import GoogleNews
import json
import time

gn = GoogleNews(lang = 'en', country = 'US')
top = gn.top_news()

entries = top["entries"]
count = 0
for entry in entries:
  count = count + 1

  keys_view = entry.keys()
#  print(keys_view)

#dict_keys(['title', 'title_detail', 'links', 'link', 'id', 'guidislink', 'published', 'published_parsed', 'summary', 'summary_detail', 'source', 'sub_articles'])
  print(
    str(count) + ". " + entry["title"]
  )

  print("\nlink ---------------------------------------------------------\n")

  print(
     entry["link"]
  )

  print("\nsummar ---------------------------------------------------------\n")

  print(
     entry["summary"]
  )

  print("\nsummary_detail ---------------------------------------------------------\n")

  print(
     str(entry["summary_detail"])
  )

  print("\nsource---------------------------------------------------------\n")

  print(
     str(entry["source"])
  )

  print("\nsub_articles---------------------------------------------------------\n")

  print(
     str(entry["sub_articles"])
  )

  print("\npublished_parsed---------------------------------------------------------\n")

  print(
     str(entry["published_parsed"])
  )

  print("\n---------------------------------------------------------\n")

  print(
     str(entry["published_parsed"]) + entry["published"]
  )

  print("\n\n")
#  time.sleep(0.25)


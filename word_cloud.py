import numpy as np
import pickle
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# Unpickling dataframe
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)
df = df[(df["Training company"] == "Entertainment 720")]

# Concatenates all the reviews into a single string
text = " ".join(review for review in df['Review'])

# Add some extra stopwords
stopwords = set(STOPWORDS)
stopwords.update(["trainer", "course", "training", "day", "material",
                  "time", "felt", "content", "made"])
# Make the word cloud
wordcloud = WordCloud(stopwords=stopwords,
                      max_words=50,
                      background_color="white",
                      mode="RGBA",
                      width=800,
                      height=400).generate(text)

# Add a colorscale
mask = np.array(Image.open("Data/cloud_colorscale.png"))
image_colors = ImageColorGenerator(mask)
# Show word cloud and save to png
#.recolor(color_func=image_colors)
plt.figure(figsize=[7,7])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
wordcloud.to_file("Data/word_cloud.png")
plt.show()

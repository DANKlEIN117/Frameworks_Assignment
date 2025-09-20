import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Title
st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

# Load data
df = pd.read_csv('metadata.csv')
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df_clean = df.dropna(subset=['title', 'publish_time'])

# Interactive year slider
year_range = st.slider("Select Year Range", int(df_clean['year'].min()), int(df_clean['year'].max()), (2020, 2021))
df_filtered = df_clean[(df_clean['year'] >= year_range[0]) & (df_clean['year'] <= year_range[1])]

# Display number of publications
st.write(f"Number of papers: {df_filtered.shape[0]}")

# Publications by year chart
year_counts = df_filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis", ax=ax)
ax.set_title("Publications by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Sample of data
st.subheader("Sample Papers")
st.dataframe(df_filtered[['title', 'journal', 'year']].head(10))

# Word Cloud
titles = ' '.join(df_filtered['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
fig_wc, ax_wc = plt.subplots(figsize=(10,5))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_json('lds-scriptures-json.txt')
df = df[['volume_title', 'book_title', 'verse_title', 'scripture_text']]
df = df[df['volume_title'] == 'Book of Mormon']

# st.set_page_config(page_title='Book of Mormon', layout='wide')
# Streamlit app
st.title('Book of Mormon Analysis')


# Create a function to filter by phrase
def phrase_filter(df, phrase):
    return df[df['scripture_text'].str.contains(phrase, case=False)]


# Get user input
phrase = st.text_input('Enter a phrase to search for')

# Filter the dataframe for the inputted phrase
df_filtered = df[df['scripture_text'].str.contains(phrase)]

# Group the filtered dataframe by book_title and count occurrences of phrase
df_grouped = df_filtered.groupby(['book_title'])['scripture_text'].apply(
    lambda x: x.str.contains(phrase).sum()
).reset_index(name='count')

# Create bar chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(df_grouped['book_title'], df_grouped['count'])
ax.set_xlabel('Occurrences')
ax.set_ylabel('Book')
ax.set_title(f'Occurrences of "{phrase}" by Book')

# Show the bar chart and table
st.pyplot(fig)
st.text('Number of occurrences: '+str(len(df_filtered)))
st.dataframe(df_filtered[['verse_title', 'scripture_text']],use_container_width=True)

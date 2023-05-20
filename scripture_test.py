import streamlit as st
import pandas as pd
import altair as alt
import re

df = pd.read_json('lds-scriptures-json.txt')
df = df[['volume_title', 'book_title', 'verse_title', 'scripture_text']]

st.set_page_config(layout='wide')

# Streamlit app
st.title('Scripture Analysis')

with st.sidebar:
    book_selection = st.multiselect(
        'Choose your book volume:',
        ['Old Testament', 'New Testament', 'Book of Mormon',
         'Doctrine and Covenants', 'Pearl of Great Price']
    )

# Create a function to filter by phrase and book volume
def filter_data(df, phrase, book_volume):
    clean_phrase = re.sub(r'[^\w\s]', '', phrase).lower()

    if not book_volume:  # Check if any book is selected
        filtered_df = df
    else:
        filtered_df = df[df['volume_title'].isin(book_volume)]

    return filtered_df[
        filtered_df['scripture_text'].str.replace(r'[^\w\s]', '', regex=True).str.lower().str.contains(clean_phrase, case=False)
    ]

# Get user input
phrase = st.text_input('Enter a phrase to search for')

# Filter the dataframe for the inputted phrase and selected book volume
df_filtered = filter_data(df, phrase, book_selection)

df_grouped = df_filtered.groupby('book_title')['scripture_text'].count().reset_index(name='count')

# Create bar chart
interval = alt.selection_single()
fig = alt.Chart(df_grouped).mark_bar().encode(
    x='count:Q',
    y=alt.Y('book_title', sort='-x')
).add_selection(
    interval
)

text = fig.mark_text(
    align='right',
    baseline='middle',
    dy=-5
).encode(
    text='book_title:O',
    tooltip='count:Q'
)

fig_labels = (fig + text).properties(
    width=alt.Step(50)
)

# Show the bar chart and table
st.altair_chart(fig, use_container_width=True)
st.text('Number of occurrences: ' + str(len(df_filtered)))
st.dataframe(df_filtered[['verse_title', 'scripture_text']], use_container_width=True)


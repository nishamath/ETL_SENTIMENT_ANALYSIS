import pandas as pd
import streamlit as st
from textblob import TextBlob
import time

# Set the title of the app
st.title("Streaming Data with Sentiment Analysis on Title and Description")

# Path to your CSV file (ensure it's the correct path to your data)
csv_file = "/home/nisha/PycharmProjects/Api_task/DbeaverExport-data.csv"

# Function to analyze sentiment and get polarity score
def analyze_sentiment(text):
    analysis = TextBlob(str(text))  # Convert to string to handle missing values
    polarity = analysis.sentiment.polarity  # Get the polarity score
    sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    return sentiment, polarity

# Initialize session state to store streamed data
if "streamed_data" not in st.session_state:
    st.session_state["streamed_data"] = pd.DataFrame()  # Empty DataFrame to store chunks

# Stream the data in chunks
try:
    for chunk in pd.read_csv(csv_file, chunksize=10):  # Process 10 rows at a time
        # Perform sentiment analysis on the 'title' column
        if "title" in chunk.columns and "description" in chunk.columns:
            # Apply sentiment analysis and get both sentiment and polarity score
            chunk[["Sentiment", "Polarity"]] = chunk["title"].apply(lambda text: pd.Series(analyze_sentiment(text)))

            # Append the new chunk to session state
            st.session_state["streamed_data"] = pd.concat(
                [st.session_state["streamed_data"], chunk], ignore_index=True
            )

            # Display the cumulative table with all chunks, including polarity
            st.subheader("Cumulative Data with Sentiment Analysis")
            st.write(st.session_state["streamed_data"][["title", "description", "Sentiment", "Polarity"]])  # Show title, description, sentiment, and polarity
        else:
            st.warning("'title' or 'description' column not found in the data!")

        time.sleep(2)  # Add delay for streaming effect

    st.success("All data streamed successfully!")
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# End-to-End Sentiment Analysis Pipeline

The data pipeline is designed to fetch, process, and analyze the sentiment of news articles using Apache Kafka, AWS services, and other modern tools. Below is a step-by-step breakdown of the pipeline's components and functionality.

##ARCHITECTURE

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Architecture.jpeg)

 The workflow begins with the News API, which retrieves news articles from external sources. These raw articles are sent to AWS Lambda, a serverless compute service, which processes the incoming data. Lambda is responsible for transforming the raw data into a more structured and usable format. Once processed, the data is integrated into the pipeline by being sent to Kafka, a distributed streaming platform.

Kafka acts as a message broker and enables real-time data streaming between different components in the architecture. It ensures that the data processed by Lambda is distributed to the relevant systems for further actions. Kafka not only facilitates seamless communication but also ensures scalability and fault tolerance in the data flow.

From Kafka, the processed data is either directed toward Amazon RDS for real-time storage and analysis or stored in Amazon S3  in json format for archival and further processing.

##S3 BUCKET

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/s3_output.jpeg)
The processed data is sent to Amazon S3, where it is stored for further analysis. Using Spark Streaming, the data is accessed from the S3 bucket for real-time processing and transformations. The results of this processing are then visualized in DBeaver, which connects to the data pipeline to enable easy querying and exploration of the processed data.

#RDS-DBEAVER OUTPUT

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Dbeaver_output.png)

The Streamlit app reads the CSV file in parts and analyzes the "title" column for sentiment and polarity. It adds each part to a live-updating table that shows the title, description, sentiment (Positive, Negative, or Neutral), and polarity. The app updates every 2 seconds, creating a streaming effect. Errors or missing data show warnings, and a success message appears when processing is complete.

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Local_streamlit.png)



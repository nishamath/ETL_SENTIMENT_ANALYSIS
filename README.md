# End-to-End Sentiment Analysis Pipeline

The data pipeline is designed to Extract, Transform, and Analyze the sentiment of news articles using Apache Kafka, AWS services, and other modern tools. Below is a step-by-step breakdown of the pipeline's components and functionality.

ARCHITECTURE
------------------

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Architecture.jpeg)

 The workflow begins with the News API, which retrieves news articles from external sources. These raw articles are sent to AWS Lambda, a serverless compute service responsible for transforming the data into a structured and usable format.The processed data is then sent to Apache Kafka, a distributed streaming platform that acts as a message broker, enabling real-time data streaming between components. Kafka ensures seamless communication, scalability, and fault tolerance.From Kafka, the data flows to either Amazon RDS for real-time storage and analysis or Amazon S3 in JSON format for archival and further processing.
 
S3 BUCKET
---------------

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/s3_output.jpeg)
*The processed data is sent to Amazon S3, where it is stored for further analysis. Using Spark Streaming, the data is accessed from the S3 bucket for real-time processing and transformations.

DBEAVER OUTPUT
---------------

*The data stored in Amazon RDS is accessed and managed using DBeaver, a database management tool. This enables easy querying, visualization, and analysis of the stored data for further insights and operations.

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Dbeaver_output.png)

The Streamlit app reads the CSV file in parts and analyzes the "title" column for sentiment and polarity. It adds each part to a live-updating table that shows the title, description, sentiment (Positive, Negative, or Neutral), and polarity. The app updates every 2 seconds, creating a streaming effect. Errors or missing data show warnings, and a success message appears when processing is complete.

LOCAL STREAMLIT(8501)
----------------------

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Local_streamlit.png)

*Developed the Streamlit app locally using essential libraries like pandas for data manipulation, streamlit for the interactive dashboard, and textblob for sentiment analysis. After testing and ensuring the app worked correctly,moved on to containerizing it.

*created a Dockerfile. This script defines how the Streamlit app should be packaged into a Docker container, specifying the required dependencies and how the app should run. This step is 
essential for deploying the app consistently across different environments. This created a container image with the Streamlit app and its dependencies, ready for deployment. Checked the docker image using diffrent port 8503.

DOCKER IMAGE
-------------
 
![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Docker%20Image.jpeg)
 
DASHBOARD (8051)
----------------
 

*The Docker image is pushed to Amazon Elastic Container Registry (ECR) using the docker push command, making it available for deployment in AWS ECS.

*The Docker containers are managed using AWS ECS Fargate, a serverless container management service. To run the pipeline, a Fargate cluster, task definition, and services are created.

*The sentiment analysis results are presented on an interactive dashboard, accessible via a public IP address. This dashboard provides users with valuable insights into news sentiment trends.
![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Dashboard(8051).png)




# Tools & Technologies Used:

Languages: Python,TextBlob,SQL

ETL Tools: Apache Kafka, AWS Lambda

Databases: PostgreSQL (Amazon RDS), Amazon S3

Visualization: Streamlit, DBeaver

Deployment: Docker, Amazon ECS (Fargate), Amazon ECR














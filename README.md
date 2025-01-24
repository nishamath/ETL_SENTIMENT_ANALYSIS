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

#LOCAL STREAMLIT(8501)

![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Local_streamlit.png)

Developed the Streamlit app locally using essential libraries like pandas for data manipulation, streamlit for the interactive dashboard, and textblob for sentiment analysis. After testing and ensuring the app worked correctly,moved on to containerizing it.

*created a Dockerfile. This script defines how the Streamlit app should be packaged into a Docker container, specifying the required dependencies and how the app should run. This step is 
 essential for deploying the app consistently across different environments. This created a container image with the Streamlit app and its dependencies, ready for deployment.

 
 ##DASHBOARD (8051)
 
![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Docker%20Image.jpeg)

Pushed the Docker image to Amazon Elastic Container Registry (ECR).the docker push command to upload it to ECR, making it available for use in AWS ECS.
The Docker containers are managed on AWS ECS Fargate, a serverless container management service. To run the pipeline, a Fargate cluster, task definition, and services are created.
The sentiment analysis results are displayed on an interactive dashboard accessible via a public IP address, providing users with valuable insights into news sentiment trends.
![Architecture](https://github.com/nishamath/ETL_SENTIMENT_ANALYSIS/blob/main/IMAGES/Dashboard(8051).png)














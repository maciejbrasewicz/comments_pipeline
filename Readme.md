# Comments Data Pipeline

## Overview

This project is a data pipeline that fetches comments from the JSONPlaceholder API (https://jsonplaceholder.typicode.com/), stores the JSON data as newline-delimited JSON in Google Cloud Storage (GCS), and writes the data to a BigQuery table. The pipeline is built using Apache Beam and is designed to be run on Google Cloud Dataflow.

![Screenshot from 2023-04-24 15-53-27](https://user-images.githubusercontent.com/49028274/234024879-b23ce6f6-91c2-4b5c-a935-79cf8bfaf165.png)


## Prerequisites

- Python 3.6 or higher
- Apache Beam Python SDK
- Google Cloud SDK

## Getting Started

1. Clone the repository and navigate to the project directory:

`git clone https://github.com/your_username/comments_pipeline.git`

`cd comments_pipeline`


2. Create and activate a virtual environment:

`python3 -m venv venv`

`source venv/bin/activate`


3. Install the required dependencies:

`pip install -r requirements.txt`


4. Set up the Google Cloud SDK:

- [Install the Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Initialize the SDK](https://cloud.google.com/sdk/docs/initializing)

5. Create a Google Cloud Storage bucket and a BigQuery dataset:

- [Create a GCS bucket](https://cloud.google.com/storage/docs/creating-buckets)
- [Create a BigQuery dataset](https://cloud.google.com/bigquery/docs/datasets)

## Running the Pipeline

To run the pipeline, execute the following command:

`python3 fetch_comments_beam.py --project PROJECT_ID --region REGION --output PROJECT:DATASET.TABLE --gcs_location gs://your-bucket/temp-folder`



Replace the following placeholders with your own values:

- `PROJECT_ID`: Your Google Cloud project ID
- `REGION`: The desired Google Cloud region (e.g., `us-central1`)
- `PROJECT`: Your Google Cloud project ID
- `DATASET`: Your BigQuery dataset ID
- `TABLE`: The desired BigQuery table name
- `your-bucket`: The name of your GCS bucket

## Data Schema

The BigQuery table will have the following schema:

| Column  | Type    | Description                                   |
| ------- | ------- | --------------------------------------------- |
| postId  | INTEGER | The ID of the post the comment belongs to     |
| id      | INTEGER | The unique ID of the comment                  |
| name    | STRING  | The name of the commenter                     |
| email   | STRING  | The email address of the commenter            |
| body    | STRING  | The text content of the comment               |

## License

This project is licensed under the [MIT License](LICENSE).

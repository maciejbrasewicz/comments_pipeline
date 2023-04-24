import argparse
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
import requests

def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        dest='output',
        required=True,
        help='Output BigQuery table for results specified as: PROJECT:DATASET.TABLE')
    parser.add_argument(
        '--gcs_location',
        dest='gcs_location',
        required=True,
        help='GCS location to store temporary files.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
    pipeline_options.view_as(beam.options.pipeline_options.GoogleCloudOptions).temp_location = known_args.gcs_location

    def fetch_comments(_):
        return requests.get('https://jsonplaceholder.typicode.com/comments').json()

    with beam.Pipeline(options=pipeline_options) as p:
        comments = (
            p
            | 'Create single item' >> beam.Create([None])
            | 'Fetch comments' >> beam.FlatMap(fetch_comments)
        )

        _ = (
            comments
            | 'Write to GCS' >> beam.io.WriteToText(known_args.gcs_location + '/temp_comments', file_name_suffix='.jsonl', num_shards=1)
        )

        _ = (
            comments
            | 'Format output' >> beam.Map(lambda comment: {'postId': comment['postId'], 'id': comment['id'], 'name': comment['name'], 'email': comment['email'], 'body': comment['body']})
            | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                known_args.output,
                schema='postId:INTEGER, id:INTEGER, name:STRING, email:STRING, body:STRING',
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                method="FILE_LOADS")
        )

if __name__ == '__main__':
    run()

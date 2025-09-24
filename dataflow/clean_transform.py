import argparse
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition
from apache_beam.io.gcp.pubsub import ReadFromPubSub


class ParseAndTransform(beam.DoFn):
    def process(self, element):
        try:
            message = json.loads(element.decode('utf-8'))
            items = message.get("items", [])

            total_items = sum(item.get("qty", 0) for item in items)
            total_price = sum(item.get("price", 0.0) * item.get("qty", 0) for item in items)
            avg_price = round(total_price / total_items, 2) if total_items > 0 else 0.0

            cleaned = {
                "transaction_id": message.get("transaction_id"),
                "timestamp": message.get("timestamp"),
                "store_id": message.get("store_id"),
                "amount": message.get("amount"),
                "total_items": total_items,
                "avg_price_per_item": avg_price
            }

            yield cleaned

        except Exception as e:
            print(f"[ERROR] Could not process record: {e}")


def run(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--runner', default='DirectRunner')
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--region', default='us-central1')
    parser.add_argument('--input_topic', required=True)
    parser.add_argument('--output_table', required=True)
    parser.add_argument('--temp_location', help='GCS temp location (required for Dataflow)', default='')

    args, pipeline_args = parser.parse_known_args(argv)
    is_dataflow = args.runner == 'DataflowRunner'

    options = PipelineOptions(
        pipeline_args,
        streaming=True,
        project=args.project_id,
        region=args.region,
        runner=args.runner,
        save_main_session=True,
        **({"temp_location": args.temp_location} if is_dataflow else {})
    )

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read from PubSub" >> ReadFromPubSub(topic=args.input_topic)
            | "Parse and Transform" >> beam.ParDo(ParseAndTransform())
            | "Write to BigQuery" >> WriteToBigQuery(
                table=args.output_table,
                schema={
                    "fields": [
                        {"name": "transaction_id", "type": "STRING", "mode": "NULLABLE"},
                        {"name": "timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
                        {"name": "store_id", "type": "STRING", "mode": "NULLABLE"},
                        {"name": "amount", "type": "FLOAT", "mode": "NULLABLE"},
                        {"name": "total_items", "type": "INTEGER", "mode": "NULLABLE"},
                        {"name": "average_item_price", "type": "FLOAT", "mode": "NULLABLE"}
                    ]
                },
                create_disposition=BigQueryDisposition.CREATE_NEVER,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                custom_gcs_temp_location=args.temp_location if is_dataflow else None
            )
        )


if __name__ == '__main__':
    run()

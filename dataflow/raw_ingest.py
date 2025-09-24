import argparse
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition

class ParseRawMessage(beam.DoFn):
    def process(self, element):
        try:
            record = json.loads(element.decode("utf-8"))
            yield record
        except Exception:
            yield beam.pvalue.TaggedOutput("dead_letter", element)

def run(argv=None):
    parser = argparse.ArgumentParser()

    # Required for both local and cloud
    parser.add_argument("--runner", default="DirectRunner", help="DirectRunner or DataflowRunner")
    parser.add_argument("--project_id", required=True)
    parser.add_argument("--region", default="us-central1")
    parser.add_argument("--input_topic", required=True)
    parser.add_argument("--output_table", required=True)

    # Required for Dataflow only
    parser.add_argument("--temp_location", default="", help="GCS path for temp files (Dataflow only)")
    parser.add_argument("--dead_letter_bucket", default="", help="GCS bucket for dead-letter (Dataflow only)")

    args, pipeline_args = parser.parse_known_args(argv)

    is_dataflow = args.runner == "DataflowRunner"

    # Pipeline options
    options = PipelineOptions(
        pipeline_args,
        runner=args.runner,
        project=args.project_id,
        region=args.region,
        streaming=True,
        save_main_session=True,
        **({
            "temp_location": args.temp_location
        } if is_dataflow else {})
    )

    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as p:
        messages = (
            p
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=args.input_topic)
            | "Parse messages" >> beam.ParDo(ParseRawMessage()).with_outputs("dead_letter", main="parsed")
        )

        # Parsed (valid) messages → BigQuery (sales_raw)
                # Parsed (valid) messages → BigQuery (sales_raw)
        messages.parsed | "Write to BigQuery" >> WriteToBigQuery(
            args.output_table,
            schema={
                "fields": [
                    {"name": "transaction_id", "type": "STRING", "mode": "NULLABLE"},
                    {"name": "timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
                    {"name": "store_id", "type": "STRING", "mode": "NULLABLE"},
                    {"name": "amount", "type": "FLOAT", "mode": "NULLABLE"},
                    {
                        "name": "items",
                        "type": "RECORD",
                        "mode": "REPEATED",
                        "fields": [
                            {"name": "sku", "type": "STRING", "mode": "NULLABLE"},
                            {"name": "qty", "type": "INTEGER", "mode": "NULLABLE"},
                            {"name": "price", "type": "FLOAT", "mode": "NULLABLE"},
                        ],
                    },
                ]
            },
            create_disposition=BigQueryDisposition.CREATE_NEVER,
            write_disposition=BigQueryDisposition.WRITE_APPEND,
        )


        # Malformed → GCS only if on Dataflow
        if is_dataflow and args.dead_letter_bucket:
            messages.dead_letter | "Write dead letters" >> beam.io.WriteToText(
                f"gs://{args.dead_letter_bucket}/deadletter/raw_ingest",
                file_name_suffix=".json"
            )
        else:
            # Just print malformed to console when running locally
            messages.dead_letter | "Print malformed" >> beam.Map(lambda x: print(f"[Malformed] {x}"))

if __name__ == "__main__":
    run()

# 🧠 Sales Analytics Data Pipeline on GCP

This project demonstrates an **end-to-end real-time data pipeline** on Google Cloud Platform (GCP), built for **Sales Analytics**. It includes raw ingestion, transformation, and loading into BigQuery for real-time analysis.

---

## 📌 Project Structure

```bash
SalesAnalytics/
│
├── terraform/                   # Infrastructure as Code (Pub/Sub, BigQuery, IAM, etc.)
│
├── dataflow/
│   ├── raw_ingest/              # Ingests raw sales data from Pub/Sub → BigQuery (sales_raw)
│   │   └── raw_ingest.py
│   │
│   ├── clean_transform/         # Batch cleaning: BigQuery (sales_raw) → BigQuery (sales_cleaned)
│   │   └── clean_transform.py
│   │
│   └── stream_clean_transform/  # Real-time cleaning: Pub/Sub → Dataflow → BigQuery (sales_cleaned)
│       └── clean_streaming.py
│
├── README.md                    # You're here!
└── .gitignore

1️⃣ Raw Ingestion (Streaming)

Reads sales data from Pub/Sub topic: retail-sales-stream

Stores raw JSON into BigQuery table: sales_data.sales_raw

Purpose: Store raw data for audit, replay, debugging

2️⃣ Clean Transform (Streaming)

Reads from same Pub/Sub topic

Applies transformation and cleaning:

Calculates total items per transaction

Computes average price per item

Writes to BigQuery table: sales_data.sales_cleaned

Used for real-time dashboards & analytics




Enable these APIs:

pubsub.googleapis.com

bigquery.googleapis.com

dataflow.googleapis.com

iam.googleapis.com



``` terraform init ```

``` terraform apply -var="project_id=your-project-id" -var="region=us-central1" ```



Test data simulator

> cd pubsub_simulator

> pip install -r requirements.txt

> gcloud auth application-default login (Set your GCP credentials (if not already using ADC):)

>
 ``` python simulate_transactions.py --project_id="your-gcp-project-id" --topic_id="retail-sales-stream" ```

_________!!!!_______
(Optional, for Production): Use the Terraform-created Service Account

You can also download the key file for the pubsub-simulator service account and authenticate like this:

export GOOGLE_APPLICATION_CREDENTIALS="/path/to/simulator-key.json"


We'll handle that when we automate more later.
___________________



TEST raw ingestion dataflow:

python raw_ingest.py \
  --runner=DirectRunner \
  --project_id=your-project-id \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_raw


python raw_ingest.py \
  --runner=DataflowRunner \
  --project_id=your-project-id \
  --region=us-central1 \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_raw \
  --temp_location=gs://your-bucket/tmp \
  --dead_letter_bucket=your-bucket


Test transform pipeline dataflow:

python clean_streaming.py \
  --runner=DirectRunner \
  --project_id=your-project-id \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_cleaned


python clean_transform.py \
  --runner=DataflowRunner \
  --project_id=your-project-id \
  --region=us-central1 \
  --output_table=your-project-id:sales_data.sales_cleaned \
  --temp_location=gs://your-bucket/tmp \
  --dead_letter_bucket=your-bucket


Security Best Practices

Use separate service accounts for pipelines with least-privilege access

Set IAM roles using Terraform (roles/pubsub.subscriber, roles/bigquery.dataEditor)

Ensure Cloud Audit Logs are enabled

Store secrets using Secret Manager (if needed)

♻️ Scalability & Resilience

Pub/Sub ensures decoupled ingestion (auto-scales)

Dataflow auto-scales with load

BigQuery supports high-throughput streaming inserts

Raw layer ensures recovery and reprocessing

Optional dead-letter queues can be added

🛠️ To Do / Enhancements

 Add Dead-letter bucket for malformed messages

 Add Airflow/Cloud Scheduler for batch job

 Add unit tests for transformations

 Add CI/CD for Terraform + Dataflow deployment

 Add Looker dashboards





    

   

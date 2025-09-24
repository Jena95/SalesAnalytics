# 🧠 Sales Analytics Real-Time Data Pipeline on GCP

This project implements an **end-to-end real-time data pipeline** on **Google Cloud Platform (GCP)** for sales analytics use cases. It supports raw data ingestion, real-time transformation, and storage in BigQuery for analytics and dashboarding.

---

## 📦 Features

- 🔄 **Real-time streaming ingestion** using Pub/Sub
- 📥 **Raw event storage** in BigQuery (`sales_raw`) for audit & replay
- 🧹 **Real-time transformation** via Dataflow & Apache Beam
- 📊 **Cleaned data** loaded into BigQuery (`sales_cleaned`)
- ☁️ Fully automated provisioning using **Terraform**
- 🔒 Secure and scalable architecture with best practices

---

## 🧱 Project Structure

```bash
SalesAnalytics/
│
├── terraform/                   # IaC for Pub/Sub, BigQuery, IAM roles, etc.
│
├── dataflow/
│   ├── raw_ingest/              # Ingests raw data from Pub/Sub → BQ (sales_raw)
│   │   └── raw_ingest.py
│   │
│   ├── clean_transform/         # Batch clean: BQ (sales_raw) → BQ (sales_cleaned)
│   │   └── clean_transform.py
│   │
│   └── stream_clean_transform/  # Real-time clean: Pub/Sub → Dataflow → BQ (sales_cleaned)
│       └── clean_streaming.py
│
├── pubsub_simulator/            # Simulates transaction data to Pub/Sub
├── README.md
└── .gitignore



______________________________________________________________


📈 Pipeline Overview
1️⃣ Raw Ingestion (Streaming)

Source: Pub/Sub topic retail-sales-stream

Sink: BigQuery table sales_data.sales_raw

Purpose: Store unprocessed JSON events for auditing, replay, and recovery

2️⃣ Real-Time Transformation (Streaming)

Source: Same Pub/Sub topic

Transformations:

Compute total items per transaction

Compute average price per item

Sink: BigQuery table sales_data.sales_cleaned

Purpose: Enables near real-time dashboarding & insights

3️⃣ Batch Transformation (Optional)

Source: BigQuery sales_raw

Sink: BigQuery sales_cleaned

Use Case: Backfills, historical reprocessing

⚙️ Setup Instructions
✅ Prerequisites

Ensure the following GCP services are enabled:

pubsub.googleapis.com

bigquery.googleapis.com

dataflow.googleapis.com

iam.googleapis.com

Install required tools:

# Install Apache Beam
pip install apache-beam[gcp]

# Install Terraform
https://developer.hashicorp.com/terraform/install

🚀 Step 1: Deploy Infrastructure with Terraform
cd terraform
terraform init
terraform apply -var="project_id=your-project-id" -var="region=us-central1"

🧪 Step 2: Test Data Generator (Pub/Sub Simulator)
cd pubsub_simulator
pip install -r requirements.txt

# Authenticate to GCP if not already
gcloud auth application-default login

# Send sample transactions
python simulate_transactions.py \
  --project_id="your-project-id" \
  --topic_id="retail-sales-stream"


✅ Optional (for production):
Use the Terraform-created service account and authenticate:

export GOOGLE_APPLICATION_CREDENTIALS="/path/to/simulator-key.json"

🔁 Run Pipelines
📥 Raw Ingestion (from Pub/Sub → BigQuery sales_raw)
▶️ DirectRunner (Local)
python raw_ingest.py \
  --runner=DirectRunner \
  --project_id=your-project-id \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_raw

☁️ Dataflow Runner (Production)
python raw_ingest.py \
  --runner=DataflowRunner \
  --project_id=your-project-id \
  --region=us-central1 \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_raw \
  --temp_location=gs://your-bucket/tmp

🧹 Real-Time Clean Transform (Pub/Sub → Dataflow → BigQuery sales_cleaned)
▶️ DirectRunner
python clean_streaming.py \
  --runner=DirectRunner \
  --project_id=your-project-id \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_cleaned

☁️ Dataflow Runner
python clean_streaming.py \
  --runner=DataflowRunner \
  --project_id=your-project-id \
  --region=us-central1 \
  --input_topic=projects/your-project-id/topics/retail-sales-stream \
  --output_table=your-project-id:sales_data.sales_cleaned \
  --temp_location=gs://your-bucket/tmp

🧼 Optional: Batch Cleaning Pipeline (sales_raw → sales_cleaned)
python clean_transform.py \
  --runner=DataflowRunner \
  --project_id=your-project-id \
  --region=us-central1 \
  --output_table=your-project-id:sales_data.sales_cleaned \
  --temp_location=gs://your-bucket/tmp

🔐 Security Best Practices

🔒 Use separate service accounts with least-privilege access

✅ Assign IAM roles via Terraform:

roles/pubsub.subscriber

roles/bigquery.dataEditor

🧾 Enable Cloud Audit Logs

🔑 Use Secret Manager for secure credentials (if needed)

♻️ Scalability & Reliability
Component	Benefit
Pub/Sub	Decouples ingestion, auto-scales with message volume
Dataflow	Fully managed streaming engine, handles load spikes
BigQuery	Optimized for high-speed streaming inserts
Raw Layer	Ensures reprocessing, debugging, and long-term storage
Dead-letter handling	(Planned) Capture failed records for future inspection
📊 Optional: Real-Time Dashboard

Use Looker Studio
 or any BI tool to visualize data from sales_data.sales_cleaned. Build dashboards showing:

Sales volume by store or time

Items per transaction

Average spend per customer

Real-time KPIs

🛠️ To-Do / Enhancements

 Add dead-letter buckets for failed records

 Schedule batch jobs using Cloud Scheduler / Airflow

 Add unit tests for transformation logic

 Implement CI/CD with GitHub Actions

 Add Looker dashboards for stakeholders

provider "google" {
  project = var.project_id
  region  = var.region
}

# Pub/Sub Topic
resource "google_pubsub_topic" "sales_stream" {
  name = "retail-sales-stream"
}

# BigQuery Dataset
resource "google_bigquery_dataset" "sales_dataset" {
  dataset_id = "sales_data"
  location   = var.region
}

# BigQuery Tables
resource "google_bigquery_table" "sales_raw" {
  dataset_id = google_bigquery_dataset.sales_dataset.dataset_id
  table_id   = "sales_raw"
  schema     = file("${path.module}/schemas/sales_raw_schema.json")
  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }
}

resource "google_bigquery_table" "sales_cleaned" {
  dataset_id = google_bigquery_dataset.sales_dataset.dataset_id
  table_id   = "sales_cleaned"
  schema     = file("${path.module}/schemas/sales_cleaned_schema.json")
  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }
}

# Service account for Pub/Sub Simulator
resource "google_service_account" "simulator" {
  account_id   = "pubsub-simulator"
  display_name = "Pub/Sub Data Simulator"
}

resource "google_project_iam_member" "simulator_pubsub_publisher" {
  project = var.project_id 
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.simulator.email}"
}

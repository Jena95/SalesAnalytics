output "pubsub_topic_name" {
  value = google_pubsub_topic.sales_stream.name
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.sales_dataset.dataset_id
}

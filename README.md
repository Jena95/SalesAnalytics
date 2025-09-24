Enable APIs for resources to be created by Terraform:

gcloud services enable iam.googleapis.com

gcloud services enable cloudresourcemanager.googleapis.com

``` terraform init 
```

``` terraform apply -var="project_id=brave-reason-421203" -var="region=us-central1"
 ```

Test data simulator

> cd pubsub_simulator

> pip install -r requirements.txt

> gcloud auth application-default login (Set your GCP credentials (if not already using ADC):)

> ``` 
python simulate_transactions.py --project_id="your-gcp-project-id" --topic_id="retail-sales-stream" 
```

_________!!!!_______
(Optional, for Production): Use the Terraform-created Service Account

You can also download the key file for the pubsub-simulator service account and authenticate like this:

export GOOGLE_APPLICATION_CREDENTIALS="/path/to/simulator-key.json"


We'll handle that when we automate more later.
___________________



TEST dataflow:

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






    

   

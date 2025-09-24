
1. Create a Pub/Sub topic

install pubsub library if not available

    pip install google-cloud-pubsub 

Create a Pub/Sub topic

    gcloud pubsub topics create retail-sales-stream

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


    

   

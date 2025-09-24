import json
import random
import time
import argparse
from datetime import datetime
from google.cloud import pubsub_v1

store_ids = ["ST01", "ST02", "ST03"]
skus = ["SKU001", "SKU002", "SKU003", "SKU004", "SKU005"]

def generate_transaction():
    items = []
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        sku = random.choice(skus)
        qty = random.randint(1, 3)
        price = round(random.uniform(5, 100), 2)
        items.append({
            "sku": sku,
            "qty": qty,
            "price": price
        })

    total_amount = round(sum(item['qty'] * item['price'] for item in items), 2)

    return {
        "transaction_id": f"TX-{random.randint(10000, 99999)}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "store_id": random.choice(store_ids),
        "amount": total_amount,
        "items": items
    }

def publish_messages(project_id, topic_id):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    while True:
        tx = generate_transaction()
        message = json.dumps(tx).encode("utf-8")
        future = publisher.publish(topic_path, data=message)
        print(f"Published: {tx['transaction_id']} at {tx['timestamp']}")
        time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate and publish retail sales transactions to Pub/Sub.")
    parser.add_argument("--project_id", required=True, help="GCP project ID")
    parser.add_argument("--topic_id", required=True, help="Pub/Sub topic ID")

    args = parser.parse_args()

    publish_messages(args.project_id, args.topic_id)

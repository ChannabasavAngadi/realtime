from flask import Flask, render_template, request
import json
import boto3

app = Flask(__name__)

# AWS Kinesis configurations
aws_access_key = "AKIAW4557RUFA4HIGOD7"
aws_secret_key = "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"
kinesis_stream_name = "click"
region_name = "us-east-1"

# Create a Kinesis client
kinesis_client = boto3.client('kinesis',
                             aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=region_name)

# Product data with initial click count set to 0
products = [
    {"name": "Mobile", "clicks": 0},
    {"name": "Laptop", "clicks": 0},
    {"name": "TV", "clicks": 0}
]

# Render the index.html template with product data
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Update click count and send data to Kinesis
@app.route('/view/<int:product_id>')
def view_item(product_id):
    if 0 <= product_id < len(products):
        products[product_id]["clicks"] += 1
        clicked_item = products[product_id]["name"]
        print(f"Clicked on {clicked_item} in terminal.")

        # Prepare the data in JSON format
        data = {
            "item": clicked_item,
            "clicks": products[product_id]["clicks"]
        }
        json_data = json.dumps(data)

        # Send data to Kinesis stream
        kinesis_client.put_record(
            StreamName=kinesis_stream_name,
            Data=json_data,
            PartitionKey="123"
        )

    return "Success"

if __name__ == '__main__':
    app.run(debug=True)

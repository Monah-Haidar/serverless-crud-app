import json
import uuid
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('http-crud-tutorial-items')

def get_items(event, context):
    try:
        response = table.scan()
        
        items = response.get('Items', [])

        body = {
            "message": "Go Serverless v4.0! Your function executed successfully!",
            "data": items,
        }

        response = {"statusCode": 200, "body": json.dumps(body, default=str)}

        return response

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Error fetching items: {str(e)}"})}
    
    


def add_item(event, context):
    try:
        
        data = json.loads(event['body'])
        item_id = str(uuid.uuid4())
        item = {
            'item_id': item_id,
            'name': data.get('name'),
            'price': data.get('price')
        }
        try:    
            table.put_item(Item=item)
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": f"Error inserting item into db:{str(e)}"})}
        
        body = {
            "message": "Item added successfully!",
            "data": {
                "item_id": item_id,
                "name": item
            }
        }

        response = {"statusCode": 200, "body": json.dumps(body)}

        return response
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Error adding item: {str(e)}"})}


def get_item(event, context):
    try:
        item_id = event['pathParameters']['item_id']
        response = table.get_item(Key={'item_id': item_id})
        item = response.get('Item')
        if not item:
            return {"statusCode": 404, "body": json.dumps({"error": "Item not found"})}
        
        body = {
            "message": "Item retrieved successfully!",
            "data": item
        }

        response = {"statusCode": 200, "body": json.dumps(body, default=str)}

        return response
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Error retrieving item: {str(e)}"})}


def update_item(event, context):
    try:
        data = json.loads(event['body'])
        item_id = event['pathParameters']['item_id']
        
        existing = table.get_item(Key={'item_id': item_id}).get('Item')
        if not existing:
            return {"statusCode": 404, "body": json.dumps({"message": "Item not found"})}
        
        response = table.update_item(
            Key={'item_id': item_id},
            UpdateExpression="set #name = :name, #price = :price",
            ExpressionAttributeNames={
                "#name": "name",
                "#price": "price"
            },
            ExpressionAttributeValues={
                ":name": data.get('name'),
                ":price": data.get('price')
            },
            ConditionExpression="attribute_exists(item_id)",
            ReturnValues="UPDATED_NEW"
        )

        updated_item = response.get('Attributes', {})
        
        body = {
            "message": "Item updated successfully!",
            "data": updated_item
        }

        response = {"statusCode": 200, "body": json.dumps(body, default=str)}

        return response
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Error updating item: {str(e)}"})}


def delete_item(event, context):
    try:
        
        item_id = event['pathParameters']['item_id']
        
        response = table.delete_item(
            Key={'item_id': item_id},
            ConditionExpression="attribute_exists(item_id)" 
        )

        
        body = {
        "message": "Item deleted successfully!",
        }

        response = {"statusCode": 200, "body": json.dumps(body)}

        return response
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Error deleting item: {str(e)}"})}

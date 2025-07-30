import json
from modules.item.services import (
    add_item_service,
    delete_item_service,
    list_item_service,
    list_items_service,
    update_item_service,
)
from modules.shared.services.logger import get_logger
from modules.shared.services.dynamodb import get_dynamodb_table

logger = get_logger(__name__)

table = get_dynamodb_table()


def get_items(event, context):
    try:
        items = list_items_service()

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Items retrieved successfully!",
                    "data": items,
                },
                default=str,
            ),
        }

    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error fetching items"}),
        }


def add_item(event, context):
    try:

        data = json.loads(event["body"])

        item = add_item_service(data)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Item added successfully!",
                    "name": item,
                },
                default=str,
            ),
        }

    except Exception as e:
        logger.error(f"Error adding item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error adding item"}),
        }


def get_item(event, context):
    try:
        item_id = event["pathParameters"]["item_id"]
        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Item ID is required"}),
            }

        item = list_item_service(item_id)
        logger.info(f"Item retrieved successfully: {item}")
        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item not found"}),
            }

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Item retrieved successfully!", "data": item}, default=str
            ),
        }

    except Exception as e:
        logger.error(f"Error retrieving item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error retrieving item"}),
        }


def update_item(event, context):
    try:
        item_id = event["pathParameters"]["item_id"]
        data = json.loads(event["body"])
        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Item ID is required"}),
            }
        if not data:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Data is required for update"}),
            }

        
        existing_item = list_item_service(item_id)
        if not existing_item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item not found"}),
            }

        updated_item = update_item_service(item_id, data)
        
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Item updated successfully!", "data": updated_item},
                default=str
            ),
        }

    except Exception as e:
        logger.error(f"Error updating item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error updating item"}),
        }


def delete_item(event, context):
    try:
        item_id = event["pathParameters"]["item_id"]
        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Item ID is required"}),
            }
        
        existing_item = list_item_service(item_id)
        if not existing_item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item not found"}),
            }

        response = delete_item_service(item_id)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Item deleted successfully!",
                },
                default=str
            ),
        }

    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error deleting item"}),
        }

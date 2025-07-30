import uuid
from modules.shared.services.logger import get_logger
from modules.shared.services.dynamodb import get_dynamodb_table


logger = get_logger(__name__)

table = get_dynamodb_table()


def list_items_service():
    response = table.scan()
    logger.info("Items retrieved successfully")
    logger.info(f"Items: {response.get('Items', [])}")
    return response.get("Items", [])


def add_item_service(item):
    item_id = str(uuid.uuid4())
    item = {
        "item_id": item_id,
        "name": item.get("name"),
        "price": item.get("price"),
    }
    table.put_item(Item=item)
    logger.info(f"Item added successfully: {item}")
    return item


def list_item_service(item_id):
    response = table.get_item(Key={"item_id": item_id})
    return response.get("Item")


def update_item_service(item_id, item):
    response = table.update_item(
        Key={"item_id": item_id},
        UpdateExpression="set #name = :name, #price = :price",
        ExpressionAttributeNames={"#name": "name", "#price": "price"},
        ExpressionAttributeValues={
            ":name": item.get("name"),
            ":price": item.get("price"),
        },
        ConditionExpression="attribute_exists(item_id)",
        ReturnValues="UPDATED_NEW",
    )
    return response.get("Attributes", {})


def delete_item_service(item_id):
    return table.delete_item(
        Key={"item_id": item_id}, ConditionExpression="attribute_exists(item_id)"
    )

import uuid
from modules.shared.services.logger import get_logger
from modules.shared.services.dynamodb import get_dynamodb_table


class ItemsService:
    def __init__(self):
        self.table = get_dynamodb_table()
        self.logger = get_logger(__name__)
        
    def list_items(self):
        response = self.table.scan()
        self.logger.info("Items retrieved successfully")
        self.logger.info(f"Items: {response.get('Items', [])}")
        return response.get("Items", [])

    def add_item(self, item):
        item_id = str(uuid.uuid4())
        item = {
            "item_id": item_id,
            "name": item.get("name"),
            "price": item.get("price"),
        }
        self.table.put_item(Item=item)
        self.logger.info(f"Item added successfully: {item}")
        return item
    
    def list_item(self, item_id):
        response = self.table.get_item(Key={"item_id": item_id})
        return response.get("Item")
    
    def update_item(self, item_id, item):
        response = self.table.update_item(
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
    
    def delete_item(self, item_id):
        return self.table.delete_item(
            Key={"item_id": item_id}, ConditionExpression="attribute_exists(item_id)"
        )



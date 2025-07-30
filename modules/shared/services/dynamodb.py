import os
import boto3

from modules.shared.services.logger import get_logger


logger = get_logger(__name__)

def get_dynamodb_table():
    table_name = os.getenv("DYNAMODB_TABLE")
    logger.info(f"Using DynamoDB table: {table_name}")
    if not table_name:
        logger.error("DYNAMODB_TABLE environment variable is not set")
        raise ValueError("DYNAMODB_TABLE environment variable is not set")
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)
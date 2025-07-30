
# Python Serverless CRUD API

This project is a Python-based CRUD (Create, Read, Update, Delete) REST API built with the [Serverless Framework](https://www.serverless.com/), AWS Lambda, API Gateway, and DynamoDB. It provides endpoints to manage items in a DynamoDB table, following best practices for serverless application development.

---

## Project Overview

This application exposes a set of HTTP API endpoints for managing items (create, read, update, delete) using AWS Lambda functions. All business logic is implemented in Python, and persistence is handled by a DynamoDB table.

**Features:**
- Create a new item
- Retrieve a single item or all items
- Update an existing item
- Delete an item

**DynamoDB Table Attributes:**
- `id` (string, primary key)
- `name` (string)
- `price` (number)

All endpoints return JSON responses and follow RESTful conventions.

---

## Tech Stack

- **Python** (3.9+ recommended)
- **Serverless Framework**
- **AWS Lambda**
- **API Gateway**
- **DynamoDB**

---

## Setup Instructions

### Prerequisites

- [Node.js](https://nodejs.org/) (v14 or later)
- [Python](https://www.python.org/) (3.9 or later)
- [AWS CLI](https://aws.amazon.com/cli/) (configured with your credentials)
- [Serverless Framework CLI](https://www.serverless.com/framework/docs/getting-started/)

### 1. Install Dependencies

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Install Serverless plugins (if not already installed):

```powershell
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-offline
```

### 2. Configure AWS Credentials

Ensure your AWS credentials are set up. You can configure them using:

```powershell
aws configure
```

This will prompt you for your AWS Access Key ID, Secret Access Key, region, and output format.

### 3. Deploy the Application

Deploy all resources and functions to AWS:

```powershell
serverless deploy
```

---

## API Endpoints

All endpoints are prefixed with `/items` and operate on the DynamoDB table.

### Create Item

- **Method:** `POST`
- **Path:** `/items`
- **Description:** Create a new item. The request body should be a JSON object with `name` and `price` attributes.
- **Example Request:**
  ```json
  {
    "name": "Sample Item",
    "price": 19.99
  }
  ```
- **Example Response:**
  ```json
  {
    "id": "<generated-uuid>",
    "name": "Sample Item",
    "price": 19.99
  }
  ```

### Get All Items

- **Method:** `GET`
- **Path:** `/items`
- **Description:** Retrieve all items from the table.
- **Example Response:**
  ```json
  [
    {
      "id": "123",
      "name": "Sample Item",
      "price": 19.99
    },
    ...
  ]
  ```

### Get Item by ID

- **Method:** `GET`
- **Path:** `/items/{item_id}`
- **Description:** Retrieve a single item by its ID.
- **Example Response:**
  ```json
  {
    "id": "123",
    "name": "Sample Item",
    "price": 19.99
  }
  ```

### Update Item

- **Method:** `PUT`
- **Path:** `/items/{item_id}`
- **Description:** Update an existing item by ID. The request body should contain the fields to update (`name` and/or `price`).
- **Example Request:**
  ```json
  {
    "name": "Updated Name",
    "price": 29.99
  }
  ```
- **Example Response:**
  ```json
  {
    "id": "123",
    "name": "Updated Name",
    "price": 29.99
  }
  ```

### Delete Item

- **Method:** `DELETE`
- **Path:** `/items/{item_id}`
- **Description:** Delete an item by its ID.
- **Example Response:**
  ```json
  {
    "message": "Item deleted successfully."
  }
  ```

---

## Environment Variables

The following environment variables are required (see `serverless.yml` for configuration):

- `AWS_REGION`: AWS region where resources are deployed (e.g., `us-east-1`).
- `DYNAMODB_TABLE`: Name of the DynamoDB table (default: `http-crud-tutorial-items`).

You can set environment variables in the `provider.environment` section of `serverless.yml` or via your deployment environment.




---

## Deployment & Monitoring

### Deploy to AWS

```powershell
serverless deploy
```

### View Logs

To view logs for a specific function:

```powershell
serverless logs -f <function_name>
```

Replace `<function_name>` with the name defined in `serverless.yml`.

### Troubleshooting

- Ensure AWS credentials are configured and have sufficient permissions.
- Check the `serverless.yml` file for correct resource and function definitions.
- Use `serverless info` to view deployed endpoints and resources.
- Use `serverless invoke local --function <function_name>` to test functions locally.
- Review CloudWatch logs for detailed error messages.

---

## References

- [Serverless Framework Documentation](https://www.serverless.com/framework/docs/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [DynamoDB Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)

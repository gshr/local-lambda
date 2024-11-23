# Local AWS Lambda Development Environment

A Docker-based local development environment for AWS Lambda functions, allowing you to test and debug Lambda functions locally before deploying to AWS.

## Prerequisites

- Docker Desktop installed
- AWS CLI configured with credentials
- Python 3.12 installed
- Git (optional but recommended)

## Project Structure

```
lambda-local-dev/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── src/                   # Lambda function code
│   └── app.py            # Main Lambda handler
├── scripts/              # Utility scripts
│   └── test_lambda.py    # Test script
└── README.md             # This file
```

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd lambda-local-dev
```

2. Set up environment variables:
```bash
# Create .env file
cat > .env << EOL
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
PORT=9000
EOL
```

3. Build and start the Lambda container:
```bash
# Build the container
docker compose build

# Start the container
docker compose up -d
```

4. Test the Lambda function:
```bash
# Using curl
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# Using the test script
python scripts/test_lambda.py
```

## Development

### Updating Lambda Function

1. Edit the Lambda function in `src/app.py`
2. Changes are automatically reflected due to volume mounting
3. Test your changes using the methods below

### Adding Dependencies

1. Add new packages to `requirements.txt`
2. Rebuild the container:
```bash
docker compose down
docker compose build
docker compose up -d
```

### Testing Methods

1. Using curl:
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
    "key": "value"
}'
```

2. Using the test script:
```bash
python scripts/test_lambda.py
```

3. Using Python interactive shell:
```python
import requests
import json

def test_lambda(payload):
    url = "http://localhost:9000/2015-03-31/functions/function/invocations"
    response = requests.post(url, json=payload)
    return response.json()

# Test
result = test_lambda({"message": "hello"})
print(json.dumps(result, indent=2))
```

### Environment Variables

View current environment variables:
```bash
# All variables
docker compose exec lambda env

# Specific variable
docker compose exec lambda printenv AWS_REGION

# Filtered variables
docker compose exec lambda env | grep AWS_
```

Set environment variables:
```bash
# In command line
PORT=9001 docker compose up -d

# Using .env file
echo "PORT=9001" >> .env
docker compose up -d
```

## Common Commands

### Container Management
```bash
# Start container
docker compose up -d

# Stop container
docker compose down

# Rebuild container
docker compose build

# View logs
docker compose logs -f

# Access container shell
docker compose exec lambda bash
```

### Testing
```bash
# Run test script
python scripts/test_lambda.py

# Test with specific payload
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"message": "test"}'
```

### Debugging
```bash
# View real-time logs
docker compose logs -f

# Check container status
docker ps

# View environment variables
docker compose exec lambda env
```

## Configuration

### Docker Configuration

The `docker-compose.yml` file supports these configurations:

```yaml
version: '3.8'
services:
  lambda:
    build: .
    volumes:
      - ./src:/var/task
    ports:
      - "${PORT:-9000}:8080"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=${AWS_REGION:-us-east-1}
```

### Environment Variables

Required variables:
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_REGION`: AWS region (default: us-east-1)
- `PORT`: Local port for Lambda (default: 9000)

Optional variables:
- `DEBUG`: Enable debug mode (true/false)
- `ENVIRONMENT`: Development environment (dev/prod)

## Troubleshooting

### Common Issues

1. Container not starting:
```bash
# Check Docker logs
docker compose logs

# Verify port availability
lsof -i :9000
```

2. Permission issues:
```bash
# Fix permissions
sudo chown -R $USER:$USER .
```

3. Network issues:
```bash
# Check if container is running
docker ps

# Verify network connectivity
curl localhost:9000
```

### Error Codes

- 500: Internal server error
- 400: Bad request
- 403: Permission denied (check AWS credentials)




# Note:

###  Entry Script (entry.sh)

The entry.sh script is used for local development to simulate the AWS Lambda Runtime Interface. This script is crucial for local testing but is not needed when deploying to AWS.
```bash
#!/bin/bash
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
    exec /usr/local/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric $1
else
    exec /usr/local/bin/python -m awslambdaric $1
fi
```

Purpose of entry.sh:

- Enables local testing by simulating AWS Lambda runtime
- Manages the AWS Lambda Runtime Interface Emulator (RIE)
- Handles the transition between local and AWS environments
- Only required for local development, not for AWS deployment
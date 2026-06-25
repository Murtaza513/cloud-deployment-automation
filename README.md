# Cloud Deployment Automation

This repo is a small DevOps deployment project. It provisions an AWS VM with Terraform, configures the server with Ansible, and runs a FastAPI app with PostgreSQL using Docker Compose.

## What It Includes

- Terraform code for an AWS VPC, public subnet, security group, and EC2 instance
- Ansible playbook to install Docker and deploy the app
- FastAPI backend with a simple PostgreSQL-backed messages API
- Docker Compose setup for the API and database
- GitHub Actions workflow for tests, Docker build, and Terraform validation

## Project Layout

```text
.
|-- .github/workflows/ci.yml
|-- ansible/
|   |-- ansible.cfg
|   |-- group_vars/app_servers.yml
|   |-- inventory.ini.example
|   |-- playbook.yml
|   `-- templates/app.env.j2
|-- app/
|   |-- Dockerfile
|   |-- docker-compose.yml
|   |-- main.py
|   |-- requirements.txt
|   `-- tests/test_main.py
|-- terraform/
|   |-- main.tf
|   |-- outputs.tf
|   |-- terraform.tfvars.example
|   `-- variables.tf
`-- README.md
```

## Running Locally

The safest way to try the application is to run only the Docker Compose stack locally. This does not create any AWS resources.

```bash
cd app
cp .env.example .env
docker compose up --build
```

Open the API docs:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

Stop the containers:

```bash
docker compose down
```

Remove the local database volume as well:

```bash
docker compose down -v
```

## Deploying to AWS

Only run this section if you want to create cloud resources. AWS may charge for EC2, storage, public IPv4, or network usage depending on your account.

### 1. Prepare Terraform Variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
project_name     = "devops-portfolio"
aws_region       = "us-east-1"
instance_type    = "t2.micro"
key_pair_name    = "your-existing-aws-keypair-name"
allowed_ssh_cidr = "YOUR_PUBLIC_IP/32"
allowed_app_cidr = "0.0.0.0/0"
```

Use your own public IP for `allowed_ssh_cidr`. Avoid opening SSH to `0.0.0.0/0`.

### 2. Create the Infrastructure

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

After the apply finishes, copy the EC2 public IP from the Terraform output.

### 3. Configure Ansible

```bash
cd ../ansible
cp inventory.ini.example inventory.ini
```

Update `inventory.ini`:

```ini
[app_servers]
app ansible_host=EC2_PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/your-key.pem
```

On Linux or macOS, make sure the key has restricted permissions:

```bash
chmod 400 ~/.ssh/your-key.pem
```

### 4. Deploy the App

```bash
ansible-playbook playbook.yml
```

When the playbook finishes, the app should be available at:

```text
http://EC2_PUBLIC_IP:8000
```

## API Endpoints

- `GET /` - basic service information
- `GET /health` - health check used by Ansible
- `GET /docs` - Swagger UI
- `POST /messages` - create a message
- `GET /messages` - list messages

Example:

```bash
curl -X POST http://EC2_PUBLIC_IP:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"text":"deployed with Terraform and Ansible"}'
```

## CI

GitHub Actions runs three checks:

- FastAPI tests
- Docker image build
- Terraform formatting and validation

The workflow is defined in `.github/workflows/ci.yml`.

## Cleanup

Destroy the AWS infrastructure when you are done:

```bash
cd terraform
terraform destroy
```
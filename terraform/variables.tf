variable "project_name" {
  description = "Name prefix used for cloud resources."
  type        = string
  default     = "devops-portfolio"
}

variable "aws_region" {
  description = "AWS region where resources will be created."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR range for the project VPC."
  type        = string
  default     = "10.10.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR range for the public subnet."
  type        = string
  default     = "10.10.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance size for the application host."
  type        = string
  default     = "t2.micro"
}

variable "key_pair_name" {
  description = "Existing AWS EC2 key pair name used for SSH access."
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH into the VM. Use your public IP with /32."
  type        = string
}

variable "allowed_app_cidr" {
  description = "CIDR block allowed to access the FastAPI service."
  type        = string
  default     = "0.0.0.0/0"
}

variable "app_port" {
  description = "Application port exposed by Docker Compose."
  type        = number
  default     = 8000
}

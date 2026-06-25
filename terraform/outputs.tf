output "instance_public_ip" {
  description = "Public IP address of the application VM."
  value       = aws_instance.app.public_ip
}

output "ssh_command" {
  description = "Example SSH command for the deployed VM."
  value       = "ssh -i <path-to-private-key> ubuntu@${aws_instance.app.public_ip}"
}

output "application_url" {
  description = "FastAPI application URL after Ansible deployment."
  value       = "http://${aws_instance.app.public_ip}:${var.app_port}"
}

output "ansible_inventory_line" {
  description = "Inventory line to paste into ansible/inventory.ini."
  value       = "app ansible_host=${aws_instance.app.public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=<path-to-private-key>"
}

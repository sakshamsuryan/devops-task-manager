terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = { source = "kreuzwerker/docker", version = "~> 3.0" }
  }
}
provider "docker" {}
module "taskflow_image" {
  source = "./modules/image"
  image_name = var.image_name
  image_tag = var.image_tag
}
output "image_id" { value = module.taskflow_image.image_id }
output "image_reference" { value = module.taskflow_image.image_reference }

variable "image_name" { type = string }
variable "image_tag" { type = string }
resource "docker_image" "app" {
  name = "${var.image_name}:${var.image_tag}"
  build { context = "${path.module}/../../.." }
}
output "image_id" { value = docker_image.app.image_id }
output "image_reference" { value = docker_image.app.name }

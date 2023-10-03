variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["backpacking-app"]
}

target "backpacking-app" {
  dockerfile = "Dockerfile"
  tags = ["localhost:5000/example-app:${TAG}"]
}

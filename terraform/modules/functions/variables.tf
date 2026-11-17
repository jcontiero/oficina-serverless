variable "project_id" { type = string }
variable "region" { type = string }
variable "vpc_connector_name" { type = string }
variable "database_url_secret_name" {
  type    = string
  default = ""
}
variable "api_backend_host" {
  type    = string
  default = "api.oficina.internal"
}
variable "pubsub_topic_id" { type = string }
variable "env_suffix" {
  type    = string
  default = ""
}
variable "env_canon" {
  type    = string
  default = "homolog"
}

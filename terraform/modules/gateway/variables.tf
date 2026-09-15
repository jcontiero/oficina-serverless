variable "region" { type = string }
variable "auth_function_uri" { type = string }
variable "api_backend_host" {
  type    = string
  default = "api.oficina.internal"
}

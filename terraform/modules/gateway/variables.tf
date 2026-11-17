variable "region" { type = string }
variable "auth_function_uri" { type = string }
variable "api_backend_host" {
  type    = string
  default = "api.oficina.internal"
}
variable "billing_backend_host" {
  type    = string
  default = "billing.oficina.internal"
}
variable "execucao_backend_host" {
  type    = string
  default = "execucao.oficina.internal"
}
variable "env_suffix" {
  type    = string
  default = ""
}

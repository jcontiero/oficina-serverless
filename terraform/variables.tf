variable "project_id" {
  type    = string
  default = "fiap-project-514922"
}

variable "region" {
  type    = string
  default = "us-east1"
}

variable "environment" {
  type        = string
  description = "Ambiente de deploy (prod preserva nomes legados; homolog aplica sufixo -homolog)"
  default     = "prod"
}

variable "vpc_connector_name" {
  type        = string
  description = "Nome do Serverless VPC Access connector (criado no oficina-k8s-infra)"
  default     = "oficina-connector"
}

variable "database_url_secret_name" {
  type        = string
  description = "Nome da secret no Secret Manager com a URL do banco"
  default     = "database-url-prod"
}

variable "api_backend_host" {
  type        = string
  description = "Host interno ou IP do backend OS (oficina-api) no GKE"
  default     = "api.oficina.internal"
}

variable "billing_backend_host" {
  type        = string
  description = "Host interno ou IP do backend Billing (oficina-billing) no GKE"
  default     = "billing.oficina.internal"
}

variable "execucao_backend_host" {
  type        = string
  description = "Host interno ou IP do backend Execucao (oficina-execucao) no GKE"
  default     = "execucao.oficina.internal"
}

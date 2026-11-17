variable "project_id" {
  type    = string
  default = "pos-fiap-2026"
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
  description = "Host interno ou IP do backend GKE"
  default     = "api.oficina.internal"
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "env_suffix" {
  description = "Sufixo de ambiente (vazio para prod, -homolog para homolog)"
  type        = string
  default     = ""
}

variable "env_canon" {
  description = "Nome canonico do ambiente (homolog ou production)"
  type        = string
  default     = "homolog"
}

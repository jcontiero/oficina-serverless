data "terraform_remote_state" "network_gke" {
  backend = "gcs"
  config = {
    bucket = "fiap-project-514922-tfstate"
    prefix = "platform/network-gke"
  }
}

locals {
  env_suffix = var.environment == "prod" || var.environment == "production" ? "" : "-${var.environment}"
  env_canon  = var.environment == "prod" ? "production" : var.environment
}

module "pubsub" {
  source     = "./modules/pubsub"
  project_id = var.project_id
  env_suffix = local.env_suffix
  env_canon  = local.env_canon
}

module "auth_function" {
  source                   = "./modules/functions"
  project_id               = var.project_id
  region                   = var.region
  vpc_connector_name       = data.terraform_remote_state.network_gke.outputs.serverless_connector_name
  database_url_secret_name = var.database_url_secret_name
  api_backend_host         = var.api_backend_host
  pubsub_topic_id          = module.pubsub.topic_id
  env_suffix               = local.env_suffix
  env_canon                = local.env_canon
}

module "api_gateway" {
  source                = "./modules/gateway"
  region                = var.region
  auth_function_uri     = module.auth_function.function_uri
  api_backend_host      = var.api_backend_host
  billing_backend_host  = var.billing_backend_host
  execucao_backend_host = var.execucao_backend_host
  env_suffix            = local.env_suffix
}

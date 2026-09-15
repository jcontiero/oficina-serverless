module "pubsub" {
  source     = "./modules/pubsub"
  project_id = var.project_id
}

module "auth_function" {
  source                   = "./modules/functions"
  project_id               = var.project_id
  region                   = var.region
  vpc_connector_name       = var.vpc_connector_name
  database_url_secret_name = var.database_url_secret_name
  pubsub_topic_id          = module.pubsub.topic_id
}

module "api_gateway" {
  source            = "./modules/gateway"
  region            = var.region
  auth_function_uri = module.auth_function.function_uri
  api_backend_host  = var.api_backend_host
}

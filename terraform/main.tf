module "auth_function" {
  source                   = "./modules/functions"
  project_id               = var.project_id
  region                   = var.region
  vpc_connector_name       = var.vpc_connector_name
  database_url_secret_name = var.database_url_secret_name
}

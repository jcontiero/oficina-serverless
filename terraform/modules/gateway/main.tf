resource "google_api_gateway_api" "api" {
  provider = google-beta
  api_id   = "oficina-api-gateway"
}

resource "google_api_gateway_api_config" "config" {
  provider             = google-beta
  api                  = google_api_gateway_api.api.api_id
  api_config_id_prefix = "oficina-config-"

  openapi_documents {
    document {
      path = "openapi.yaml"
      contents = base64encode(templatefile("${path.root}/../openapi/gateway.yaml", {
        auth_function_host = replace(replace(var.auth_function_uri, "https://", ""), "http://", "")
        api_backend_host   = var.api_backend_host
      }))
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "gateway" {
  provider   = google-beta
  api_config = google_api_gateway_api_config.config.id
  gateway_id = "oficina-gateway"
  region     = var.region
}

output "gateway_hostname" {
  value = google_api_gateway_gateway.gateway.default_hostname
}
output "gateway_url" {
  value = "https://${google_api_gateway_gateway.gateway.default_hostname}"
}

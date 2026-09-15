output "function_uri" {
  value = google_cloudfunctions2_function.auth_function.service_config[0].uri
}

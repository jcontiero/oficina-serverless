output "auth_function_uri" {
  value       = module.auth_function.function_uri
  description = "URI publica da Cloud Function de autenticacao e JWKS"
}

output "api_gateway_url" {
  value       = module.api_gateway.gateway_url
  description = "URL publica oficial do API Gateway (Ponto de entrada unico)"
}

output "auth_function_uri" {
  value       = module.auth_function.function_uri
  description = "URI publica da Cloud Function de autenticacao e JWKS"
}

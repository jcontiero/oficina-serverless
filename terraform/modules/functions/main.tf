data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.root}/../src"
  output_path = "${path.module}/function-source.zip"
}

resource "google_storage_bucket" "source_bucket" {
  name          = "${var.project_id}-functions-source${var.env_suffix}"
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "source_archive" {
  name   = "auth-function-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.source_bucket.name
  source = data.archive_file.function_zip.output_path
}

resource "google_service_account" "functions_sa" {
  account_id   = "oficina-fn-${var.env_canon}-sa"
  display_name = "Runtime SA para Cloud Functions (${var.env_canon})"
}

resource "tls_private_key" "client_jwt" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "google_secret_manager_secret" "client_jwt_pem" {
  secret_id = "oficina-client-jwt-private-key-${var.env_canon}"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "client_jwt_pem" {
  secret      = google_secret_manager_secret.client_jwt_pem.id
  secret_data = tls_private_key.client_jwt.private_key_pem
}

resource "google_secret_manager_secret_iam_member" "functions_jwt_accessor" {
  secret_id = google_secret_manager_secret.client_jwt_pem.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.functions_sa.email}"
}

resource "google_cloudfunctions2_function" "auth_function" {
  name        = "oficina-auth-function${var.env_suffix}"
  location    = var.region
  description = "Cloud Function para autenticacao de clientes por CPF e JWKS"

  build_config {
    runtime     = "python312"
    entry_point = "auth_handler"
    source {
      storage_source {
        bucket = google_storage_bucket.source_bucket.name
        object = google_storage_bucket_object.source_archive.name
      }
    }
  }

  service_config {
    service_account_email          = google_service_account.functions_sa.email
    max_instance_count             = 5
    min_instance_count             = 0
    available_memory               = "256M"
    timeout_seconds                = 15
    vpc_connector                  = "projects/${var.project_id}/locations/${var.region}/connectors/${var.vpc_connector_name}"
    vpc_connector_egress_settings  = "PRIVATE_RANGES_ONLY"
    all_traffic_on_latest_revision = true

    environment_variables = {
      ENVIRONMENT             = var.env_canon
      JWT_KEY_ID              = "oficina-rsa-key-2026"
      JWT_ISSUER              = "oficina-auth-${var.env_canon}"
      JWT_AUDIENCE            = "oficina-backend-${var.env_canon}"
      OS_AUTH_LOOKUP_URL      = "https://${var.api_backend_host}/internal/clientes/autenticacao"
      OS_AUTH_LOOKUP_AUDIENCE = "https://api.oficina.internal/internal/clientes/autenticacao"
    }

    secret_environment_variables {
      key        = "JWT_PRIVATE_KEY_PEM"
      project_id = var.project_id
      secret     = google_secret_manager_secret.client_jwt_pem.secret_id
      version    = "latest"
    }
  }

  depends_on = [
    google_secret_manager_secret_version.client_jwt_pem,
    google_secret_manager_secret_iam_member.functions_jwt_accessor,
  ]
}

resource "google_cloudfunctions2_function" "notificacoes_function" {
  name        = "oficina-notificacoes-function${var.env_suffix}"
  location    = var.region
  description = "Cloud Function para envio de notificacoes"

  build_config {
    runtime     = "python312"
    entry_point = "notificacoes_handler"
    source {
      storage_source {
        bucket = google_storage_bucket.source_bucket.name
        object = google_storage_bucket_object.source_archive.name
      }
    }
  }

  service_config {
    max_instance_count             = 2
    min_instance_count             = 0
    available_memory               = "256M"
    timeout_seconds                = 60
    vpc_connector                  = "projects/${var.project_id}/locations/${var.region}/connectors/${var.vpc_connector_name}"
    vpc_connector_egress_settings  = "PRIVATE_RANGES_ONLY"
    all_traffic_on_latest_revision = true
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = var.pubsub_topic_id
    retry_policy   = "RETRY_POLICY_DO_NOT_RETRY" # Pub/Sub já faz retry
  }
}

resource "google_cloud_run_service_iam_member" "public_invoker" {
  location = google_cloudfunctions2_function.auth_function.location
  service  = google_cloudfunctions2_function.auth_function.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.root}/../src"
  output_path = "${path.module}/function-source.zip"
}

resource "google_storage_bucket" "source_bucket" {
  name          = "${var.project_id}-functions-source"
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "source_archive" {
  name   = "auth-function-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.source_bucket.name
  source = data.archive_file.function_zip.output_path
}

resource "google_cloudfunctions2_function" "auth_function" {
  name        = "oficina-auth-function"
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
    max_instance_count             = 5
    min_instance_count             = 0
    available_memory               = "256M"
    timeout_seconds                = 15
    vpc_connector                  = "projects/${var.project_id}/locations/${var.region}/connectors/${var.vpc_connector_name}"
    vpc_connector_egress_settings  = "PRIVATE_RANGES_ONLY"
    all_traffic_on_latest_revision = true

    environment_variables = {
      JWT_KEY_ID = "oficina-rsa-key-2026"
    }

    secret_environment_variables {
      key        = "DATABASE_URL"
      project_id = var.project_id
      secret     = var.database_url_secret_name
      version    = "latest"
    }
  }
}

resource "google_cloudfunctions2_function" "notificacoes_function" {
  name        = "oficina-notificacoes-function"
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

    secret_environment_variables {
      key        = "DATABASE_URL"
      project_id = var.project_id
      secret     = var.database_url_secret_name
      version    = "latest"
    }
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

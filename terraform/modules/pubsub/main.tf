resource "google_pubsub_topic" "notificacoes" {
  name = "oficina-notificacoes-topic${var.env_suffix}"
}

resource "google_pubsub_topic" "notificacoes_dlq" {
  name = "oficina-notificacoes-dlq${var.env_suffix}"
}

resource "google_pubsub_topic" "eventos_v1" {
  name = "oficina-${var.env_canon}-eventos-v1"
}

resource "google_pubsub_topic" "eventos_v1_dlq" {
  name = "oficina-${var.env_canon}-eventos-v1-dlq"
}

resource "google_pubsub_topic" "billing_comandos_v1" {
  name = "oficina-${var.env_canon}-billing-comandos-v1"
}

resource "google_pubsub_topic" "billing_comandos_v1_dlq" {
  name = "oficina-${var.env_canon}-billing-comandos-v1-dlq"
}

resource "google_pubsub_topic" "execucao_comandos_v1" {
  name = "oficina-${var.env_canon}-execucao-comandos-v1"
}

resource "google_pubsub_topic" "execucao_comandos_v1_dlq" {
  name = "oficina-${var.env_canon}-execucao-comandos-v1-dlq"
}

# O service agent precisa publicar as mensagens que excederem as tentativas.
data "google_project" "pubsub_project" {
  project_id = var.project_id
}

resource "google_pubsub_topic_iam_member" "dead_letter_forwarder" {
  for_each = {
    eventos  = google_pubsub_topic.eventos_v1_dlq.name
    billing  = google_pubsub_topic.billing_comandos_v1_dlq.name
    execucao = google_pubsub_topic.execucao_comandos_v1_dlq.name
  }
  project = var.project_id
  topic   = each.value
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:service-${data.google_project.pubsub_project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

resource "google_pubsub_subscription" "dead_letter_retention" {
  for_each = {
    eventos  = google_pubsub_topic.eventos_v1_dlq.name
    billing  = google_pubsub_topic.billing_comandos_v1_dlq.name
    execucao = google_pubsub_topic.execucao_comandos_v1_dlq.name
  }
  name                       = "${each.value}-retention"
  topic                      = each.value
  message_retention_duration = "604800s"
  expiration_policy { ttl = "" }
}

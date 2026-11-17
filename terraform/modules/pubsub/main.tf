resource "google_pubsub_topic" "notificacoes" {
  name = "oficina-notificacoes-topic${var.env_suffix}"
}

resource "google_pubsub_topic" "notificacoes_dlq" {
  name = "oficina-notificacoes-dlq${var.env_suffix}"
}

resource "google_pubsub_topic" "notificacoes" {
  name = "oficina-notificacoes-topic"
}

resource "google_pubsub_topic" "notificacoes_dlq" {
  name = "oficina-notificacoes-dlq"
}

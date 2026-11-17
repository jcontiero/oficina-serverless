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

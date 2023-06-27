variable "cloud_storage_credentials" {
    description = "Google Cloud Storage credentials"
    type = string
    default = "/service_account/cloud_storage.json"
}

variable "bigquery_credentials" {
    description = "Google Cloud BigQuery credentials"
    type = string
    default = "/service_account/bigquery.json"
}

variable "google_project" {
    description = "Google Cloud project ID"
    type = string
    default = ""
}

variable "google_region" {
    description = "Google Cloud region"
    type = string
    default = "us-central1"
}

variable "google_bucket" {
    description = "Google Cloud bucket"
    type = string
    default = ""
}

variable "bigquery_dataset" {
    description = "BigQuery dataset"
    type = string
    default = "cryptocurrency"
}

variable "name_dim" {
    type = string
    default = "name_dim"
}

variable "tag_dim" {
    type = string
    default = "tag_dim"
}

variable "name_tag" {
    type = string
    default = "name_tag"
}

variable "quote_dim" {
    type = string
    default = "quote_dim"
}

variable "date_dim" {
    type = string
    default = "date_dim"
}

variable "month_dim" {
    type = string
    default = "month_dim"
}

variable "weekday_dim" {
    type = string
    default = "weekday_dim"
}

variable "price_fact" {
    type = string
    default = "price_fact"
}

variable "trading_volume_day_fact" {
    type = string
    default = "trading_volume_day_fact"
}

variable "supply_fact" {
    type = string
    default = "supply_fact"
}

variable "rank_fact" {
    type = string
    default = "rank_fact"
}
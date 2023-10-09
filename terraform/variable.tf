variable "cloud_storage_credentials" {
    description = "Google Cloud Storage credentials"
    type = string
    default = "/service_account/cloud-storage.json"
}

variable "bigquery_credentials" {
    description = "Google Cloud BigQuery credentials"
    type = string
    default = "/service_account/bigquery.json"
}

variable "compute_engine_credentials" {
    description = "Google Cloud Compute Engine credentials"
    type = string
    default = "/service_account/compute-engine.json"
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
    default = "projects-cryptocurrency"
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

variable "day_dim" {
    type = string
    default = "day_dim"
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

variable "machine_type" {
    type = string
    default = "e2-medium"
}

variable "zone" {
    type = string
    default = "us-central1-a"
}

variable "image" {
    type = string
    default = "ubuntu-os-cloud/ubuntu-2004-lts"
}

variable "coinmarket" {
    type = string
    default = ""
}

variable "coinmarket_latest_listings" {
    type = string
    default = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
}

variable "repo" {
    type = string
    default = "https://github.com/BenGriffith/cryptocurrency.git"
}
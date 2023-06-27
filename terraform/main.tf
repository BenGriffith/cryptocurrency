terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "4.51.0"
    }
  }
}

provider "google" {
  alias = "cloud_storage_provider"
  credentials = var.cloud_storage_credentials
  project = var.google_project
  region = var.google_region
}

provider "google" {
  alias = "bigquery_provider"
  credentials = var.bigquery_credentials
  project = var.google_project
  region = var.google_region
}

resource "google_storage_bucket" "bucket" {
  name = var.google_bucket
  project = var.google_project
  location = var.google_region
  storage_class = "STANDARD"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bigquery_dataset
  project = var.google_project
  location = var.google_region
}

resource "google_bigquery_table" "name_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.name_dim
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "symbol",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "slug",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "tag_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.tag_dim
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "tag_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "tag",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "name_tag" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.name_tag
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "date_key",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "tag_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "quote_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.quote_dim
  project = var.google_project
  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "date_key"
    require_partition_filter = true
  }

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "date_key",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "quote",
    "type": "JSON",
    "mode": "REPEATED"
  }
] 
EOF
}

resource "google_bigquery_table" "date_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.date_dim
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "date_key",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "year",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "month_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "day",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "weekday_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "week_number",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "week_end",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "month_end",
    "type": "DATE",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "month_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.month_dim
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "month_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "weekday_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.weekday_dim
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "weekday_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "price_fact" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.price_fact
  project = var.google_project
  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "date_key"
    require_partition_filter = true
  }

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "date_key",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "price",
    "type": "NUMERIC",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "trading_volume_day_fact" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.trading_volume_day_fact
  project = var.google_project
  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "date_key"
    require_partition_filter = true
  }

  schema = <<EOF
  [
    {
      "name": "name_key",
      "type": "INTEGER",
      "mode": "NULLABLE"
    },
    {
      "name": "date_key",
      "type": "DATE",
      "mode": "NULLABLE"
    },
    {
      "name": "volume",
      "type": "INTEGER",
      "mode": "NULLABLE"
    }
  ]
  EOF
}

resource "google_bigquery_table" "supply_fact" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.supply_fact
  project = var.google_project
  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "date_key"
    require_partition_filter = true
  }

  schema = <<EOF
  [
    {
      "name": "name_key",
      "type": "INTEGER",
      "mode": "NULLABLE"
    },
    {
      "name": "date_key",
      "type": "DATE",
      "mode": "NULLABLE"
    },
    {
      "name": "circulating",
      "type": "INTEGER",
      "mode": "NULLABLE"
    },
    {
      "name": "total",
      "type": "INTEGER",
      "mode": "NULLABLE"
    },
    {
      "name": "max",
      "type": "INTEGER",
      "mode": "NULLABLE"
    }
  ]
  EOF
}

resource "google_bigquery_table" "rank_fact" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.rank_fact
  project = var.google_project
  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "date_key"
    require_partition_filter = true
  }

  schema = <<EOF
  [
    {
      "name": "name_key",
      "type": "INTEGER",
      "mode": "NULLABLE"
    },
    {
      "name": "date_key",
      "type": "DATE",
      "mode": "NULLABLE"
    },
    {
      "name": "rank",
      "type": "INTEGER",
      "mode": "NULLABLE"
    }
  ]
  EOF
}
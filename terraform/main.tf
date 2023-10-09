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

provider "google" {
  alias = "compute_engine_provider"
  credentials = var.compute_engine_credentials
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

  time_partitioning {
    type = "DAY"
    field = "date_key"
  }

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "STRING",
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
  }

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "STRING",
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
    "name": "day_key",
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

resource "google_bigquery_table" "day_dim" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.day_dim
  project = var.google_project
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "day_key",
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
  }

  schema = <<EOF
[
  {
    "name": "name_key",
    "type": "STRING",
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
  }

  schema = <<EOF
  [
    {
      "name": "name_key",
      "type": "STRING",
      "mode": "NULLABLE"
    },
    {
      "name": "date_key",
      "type": "DATE",
      "mode": "NULLABLE"
    },
    {
      "name": "volume",
      "type": "FLOAT",
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
  }

  schema = <<EOF
  [
    {
      "name": "name_key",
      "type": "STRING",
      "mode": "NULLABLE"
    },
    {
      "name": "date_key",
      "type": "DATE",
      "mode": "NULLABLE"
    },
    {
      "name": "circulating",
      "type": "FLOAT",
      "mode": "NULLABLE"
    },
    {
      "name": "total",
      "type": "FLOAT",
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
  }

  schema = <<EOF
  [
    {
      "name": "name_key",
      "type": "STRING",
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

resource "google_compute_instance" "crypto_instance" {
  name = "crypto-instance"
  machine_type = var.machine_type
  project = var.google_project
  zone = var.zone
  
  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  metadata = {
    startup-script = <<-EOF
      echo "-------------------------START SETUP---------------------------"
      sudo apt-get -y update

      sudo apt-get -y install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

      sudo apt -y install unzip

      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

      echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

      sudo apt-get -y update
      sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
      sudo chmod 666 /var/run/docker.sock

      sudo apt install make

      echo 'Clone git repo to GCE'
      cd /home/ubuntu && git clone ${var.repo}

      echo 'CD to cryptocurrency directory'
      cd cryptocurrency
      mv .env-template .env

      sed -i 's/COINMARKET_API_KEY=/COINMARKET_API_KEY=${var.coinmarket}/' .env
      sed -i 's,LISTINGS_LATEST_URL=,LISTINGS_LATEST_URL=${var.coinmarket_latest_listings},' .env
      sed -i 's/BUCKET=/BUCKET=${var.google_bucket}/' .env
      sed -i 's,CLOUD_STORAGE=,CLOUD_STORAGE=${var.cloud_storage_credentials},' .env
      sed -i 's,BIGQUERY=,BIGQUERY=${var.bigquery_credentials},' .env
      sed -i 's/PROJECT_ID=/PROJECT_ID=${var.google_project}/' .env

      echo 'Start containers'
      make docker-spin-up

      echo "-------------------------END SETUP---------------------------"
    EOF
  }

  network_interface {
    network = google_compute_network.vpc_network.self_link
    access_config {
    }
  }

}

resource "google_compute_network" "vpc_network" {
  name = "crypto-network"
  project = var.google_project
  auto_create_subnetworks = true
}

resource "google_compute_firewall" "ingress_firewall_rule" {
  name        = "allow-http-https-ingress"
  network     = google_compute_network.vpc_network.name
  project     = var.google_project

  direction   = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "egress_firewall_rule" {
  name        = "allow-http-https-egress"
  network     = google_compute_network.vpc_network.name
  project     = var.google_project

  direction   = "EGRESS"

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080"]
  }
}
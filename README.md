## General Info

This data pipeline pulls a list of active cryptocurrencies with the latest market data from the CoinMarketCap API and loads it into our data lake and data warehouse.

Python is used to read from CoinMarketCap API and write to our data lake, Google Cloud Storage. Shortly after writing to our data lake another process will kick off using Python to read from Google Cloud Storage, perform transformations and write to our datawarehouse, BigQuery. The `Extract/Load` process and `Tranform/Load` process are in the form of separate Docker containers on a Google Compute Engine instance. Terraform is used to provision and teardown the project infrastructure/components.

In the `Extract/Load` process, Python is used to read from the CoinMarketCap API and write to our data lake, Google Cloud Storage (GCS). Next, in the `Transform/Load` process, Python is used to read from our data lake and write to our datawarehouse, BigQuery.

The `Extract/Load` and `Transform/Load` processes are in separate docker containers on a Google Compute Engine (GCE) instance and scheduled to run daily via cron jobs. 

Terraform is used to setup and tear down pipeline components such as GCS bucket, BigQuery dataset and tables, and GCE instance/networking.


### Architecture
![architecture](/assets/architecture.png)


### Entity Relationship Diagram (Facts and Dimensions)
![erd](/assets/erd.png)


### Setup/Tear down

#### Pre-requisites
1. CoinMarketCap API Key
2. Google Cloud account
3. Service account for Google Cloud Storage
4. Service account for BigQuery
5. Service account for Compute Engine
6. Download service account keys and move to `/service_account`
- For Cloud Storage, name the file `cloud-storage.json`
- For BigQuery, name the file `bigquery.json`
- For Compute Engine, name the file `compute-engine.json`
7. Rename `.env-template` to `.env`
8. Configure `.env` with user-defined values
- For `BUCKET`, specify the GCS bucket name
- For `CLOUD_STORAGE`, specify the path to the service account key such as /service_account/cloud-storage.json
- For `BIGQUERY`, specify the path to the service account key such as /service_account/bigquery.json
9. In `/terraform/variable.tf`, configure `google_project` and `coinmarket` with user-defined values

#### Setup commands
```
$ git clone https://github.com/bengriffith/cryptocurrency.git
$ cd cryptocurrency
$ make tf-init
$ make infra-up
```

#### Tear down commands
```
$ make infra-down
```
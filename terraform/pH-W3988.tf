variable "function_phw3988" {
  type        = string
  default     = "tuya-hydrop-ph-w3988"
  
}

# Zip up the source code for ph-w3988
data "archive_file" "function_src_ph_w3988_zip" {
    type        = "zip"
    source_dir  = "${path.module}/../pH-W3988/src"
    output_path = "/tmp/${var.function_phw3988}.zip"
    excludes    = var.python_excludes
}

#copy function_src_ph_w3988_zip to souce bucket where it will be deployed from
resource "google_storage_bucket_object" "function_src_ph_w3988_zip" {
    name   = "${var.function_phw3988}-${data.archive_file.function_src_ph_w3988_zip.output_md5}.zip"
    bucket = data.google_storage_bucket.functions_src.name
    source = data.archive_file.function_src_ph_w3988_zip.output_path
}

# Create a Cloud Function that triggers on the topic
resource "google_cloudfunctions_function" "tuya_hydrop_pH_W3988" {
  name        = var.function_phw3988
  description = "Cloud function that pulls metrics from pH-W3988 sensor"
  runtime     = "python39"
  entry_point = "pull_data"
  service_account_email = google_service_account.function_sa.email

  # Use the Pub/Sub trigger
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/every-5min"
  }

  environment_variables = {
    SECRET_ID = google_secret_manager_secret.function_secret.name
  }

  # Use the default function code
  source_archive_bucket = data.google_storage_bucket.functions_src.name
  source_archive_object = google_storage_bucket_object.function_src_ph_w3988_zip.name

  depends_on = [ google_service_account.function_sa  ]
}
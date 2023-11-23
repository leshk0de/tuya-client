
variable "function_smartplug" {
  type        = string
  default     = "tuya-hydrop-smart-plug"
  
}

data "archive_file" "function_src_smart_plug_zip" {
    type        = "zip"
    source_dir  = "${path.module}/../smartPlug/src"
    output_path = "/tmp/${var.function_smartplug}.zip"
    excludes    = var.python_excludes
}


#copy function_src_smart_plug_zip to souce bucket where it will be deployed from
resource "google_storage_bucket_object" "function_src_smart_plug_zip" {
    name   = "${var.function_smartplug}-${data.archive_file.function_src_smart_plug_zip.output_md5}.zip"
    bucket = data.google_storage_bucket.functions_src.name
    source = data.archive_file.function_src_smart_plug_zip.output_path
}


#Create a Cloud Function that triggers on the topic
resource "google_cloudfunctions_function" "tuya_hydrop_smart_plug" {
  name        = var.function_smartplug
  description = "Cloud function that pulls metrics from smart plug sensor"
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
  source_archive_object = google_storage_bucket_object.function_src_smart_plug_zip.name

  depends_on = [ google_service_account.function_sa  ]
}
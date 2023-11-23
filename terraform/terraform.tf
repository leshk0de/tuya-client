# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
}


resource "google_service_account" "function_sa" {
  account_id   = "sa-${var.function_base_name}"
  display_name = "Service account for ${var.function_base_name} app"
}


# Create a Cloud Storage bucket to store function output
resource "google_storage_bucket" "function_bucket" {
  name = "${var.function_base_name}-data"
  location = "us"
}

resource "google_storage_bucket_iam_binding" "binding" {
  bucket = google_storage_bucket.function_bucket.name
  role = "roles/storage.admin"
  members = [
    "serviceAccount:${google_service_account.function_sa.email}",
  ]

  depends_on = [ google_service_account.function_sa ]
}


resource "google_secret_manager_secret" "function_secret" {
  secret_id = "${var.function_base_name}-secrets"
  replication {
    auto {}
  }

}

resource "google_secret_manager_secret_iam_binding" "binding" {
  project = var.project_id
  secret_id = google_secret_manager_secret.function_secret.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${google_service_account.function_sa.email}"
  ]
  depends_on = [ google_service_account.function_sa ]
}

# Misc list to files during deployment
variable "python_excludes" {
  description = "Files to exclude from python cloud function src directory"
  type        = list(string)
  default     = [
    ".venv",
    "README.md",
    "testing",
    "deploy.sh",
    ".env",
    "misc",
    "notes.txt",
    "__pycache__"
  ]
}

output "function-name" {
  value = google_cloudfunctions_function.tuya_hydrop_pH_W3988.name
}
output "function-trigger" {
  value = google_cloudfunctions_function.tuya_hydrop_pH_W3988.https_trigger_url
}
output "function-bucket" {
  value = google_storage_bucket.function_bucket.name
}
provider "google" {
  project = var.project_id
  region  = var.region
}
module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "~> 29.0"
  # ...cluster config...
}
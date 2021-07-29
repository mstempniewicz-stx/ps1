terraform {
  # The configuration for this backend will be filled in by Terragrunt
  backend "s3" {}
}

provider "aws" {
  region = "eu-west-1"
}

module "application" {
  source = "../../modules/app"
  application_environment = "${var.application_environment}"
  prefix = "${var.prefix}"
  key_pair_name = "${var.key_pair_name}"
  domain_name = "${var.domain_name}"
  db_password = "${var.db_password}"
}

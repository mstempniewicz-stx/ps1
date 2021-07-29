terragrunt = {
  remote_state {
    backend = "s3"

    config {
      # Bucket name where terraform remote state will be kept
      bucket         = "##replace##"
      region         = "eu-west-1"
      encrypt        = true
      # Path where terraform state will be kept, if you want more then one app in one bucket,
      # you can set ##replace## accordingly
      key            = "##replace##/${path_relative_to_include()}/terraform.tfstate"
      # Dynamodb table name used for locking (2 users can't run terraform in parallel)
      dynamodb_table = "##replace##"
    }
  }

  terraform {
    extra_arguments "secrets" {
      arguments = [
        "-var-file=${get_tfvars_dir()}/secrets.tfvars"
      ]
      commands = [
        "apply",
        "plan",
        "destroy",
        "import",
        "push",
        "refresh"
      ]
    }
  }
}

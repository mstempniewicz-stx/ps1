terraform {
  # The configuration for this backend will be filled in by Terragrunt
  backend "s3" {}
}

terragrunt = {
  include {
    path = "${find_in_parent_folders()}"
  }
}

application_environment = "staging"

# Prefix for application, mostly used for tagging purposes
# Example: myapp-staging
prefix = "##replace##"

# Access key name for application ssh, created in EC2 key pairs panel
key_pair_name = "##replace##"

# Domain name for application, there would be Route53 records created for it, domains still need to point hosted zone NS
# which needs to be done manually
# Example: "app-envname-web.zxc123.eu-west-1.elasticbeanstalk.com"
domain_name = "##replace##"

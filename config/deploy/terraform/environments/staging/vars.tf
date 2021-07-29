variable "application_environment" {
  description = "Deployment stage e.g. 'staging', 'production', 'test', 'integration'"
}

variable "prefix" {
  description = "Prefix for env resources"
}

variable "key_pair_name" {
  description = "Key pair used to access AWS instance"
}

variable "domain_name" {
  description = "Domain to be used by application"
}


##########################
# Read from secrets.tfvar
##########################
variable "db_password" {
  description = "Password for main DB"
}


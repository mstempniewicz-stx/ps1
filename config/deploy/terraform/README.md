### State

Terraform uses remote state configuration kept in s3 bucket, configuration may be found in main `terraform.tfvars` file.

### Locking

Locking is done using DynamoDB, thanks to that 2 users are not allowed to run commands simultaneously.

### Environments

Each environment has it's own directory in `environments` folder.
Secrets are kept in `secrets.tfvars` file.

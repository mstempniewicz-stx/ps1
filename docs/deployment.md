# Django React/Redux Base Project - deployment

This repository includes a boilerplate project. It uses Django as backend and React as frontend.

## Deployment with CI/CD

### Steps to configure:

-   Create new organization/project in Codeship PRO and connect it with git repository

    -   Download aes key, name it `codeship.aes` and place it in main directory of project (It cannot be commited to repo), this file is used to encrypt sensitive data for Codeship
        -   Go into projects tab in settings
        -   Choose you project
        -   Go to settings and change tab to `General`
        -   Use `Download Key` button
        -   **Do not commit key in repository!**
    -   Create Codeship environment file
        -   copy `codeship.env.sample` to `codeship.env`
        -   set variables values
        -   **Do not commit `codeship.env` in repository!**
    -   Install [jet tool](https://documentation.codeship.com/pro/jet-cli/installation/)
    -   execute in main directory
        `jet encrypt ./docker/codeship.env ./docker/codeship.env.encrypted --key-path ./codeship.aes`
    -   commit `codeship.env.encrypted` into repository

-   Create repository in [Amazon ECR (ECS)](https://eu-west-1.console.aws.amazon.com/ecs/home#/repositories)

    -   Set Repository name for your image
    -   Replace `image_name` in `codeship-steps.yml` with your image name. Sample format: `111111111111.dkr.ecr.eu-west-1.amazonaws.com/stx/web-app` where repository name is `stx/web-app`.

-   Create environment in AWS (Terraform)

    -   Prequisites

        -   Create [IAM](https://console.aws.amazon.com/iam/home) **user** for terraform and give it required permission.

            -   Assign `Programmatic access` option to it.
            -   List of required permissions, not everywhere full access is required, due to lack of time didn't select single permissions.
                -   AmazonRDSFullAccess
                -   AmazonEC2FullAccess
                -   AmazonElastiCacheFullAccess
                -   AmazonS3FullAccess
                -   AmazonDynamoDBFullAccess
                -   AWSElasticBeanstalkFullAccess
                -   AmazonVPCFullAccess
                -   AmazonRoute53FullAccess
            -   Save access key and secret key for this user
            -   Copy `codeship.env.sample` file into `codeship.env` and fill env details. (Using terraform user access details)
            -   Use jet to encrypt `codeship.env` file. `jet encrypt docker/codeship.env docker/codeship.env.encrypted`.
                Encrypted file should be committed in repository.

        -   Create `aws-elasticbeanstalk-ec2-role` **role** in [IAM](https://console.aws.amazon.com/iam/home)

            -   Type of trusted entity: `AWS Service`
            -   Service: `EC2`
            -   Required permissions:
                -   AWSElasticBeanstalkWebTier
                -   AWSElasticBeanstalkMulticontainerDocker
                -   AWSElasticBeanstalkWorkerTier
                -   AmazonEC2ContainerRegistryReadOnly - To pull image from docker repository
            -   Set Role Name to `aws-elasticbeanstalk-ec2-role`

        -   Create key-pair in [EC2](https://eu-west-1.console.aws.amazon.com/ec2/v2/home)
            -   Remember to save downloaded key somewhere, because it won't be available later.
            -   You can import existing key pair if you want

    -   Terraform

        -   Install [terraform](https://www.terraform.io/intro/getting-started/install.html) and [terragrunt](https://github.com/gruntwork-io/terragrunt)
            -   Terragrunt is wrapper package for terraform, which allows to use remote s3 state (for teams) and state locking.
            -   **Remember to always use terragrunt!!!**
            -   There is a great tutorial series on medium.com: https://blog.gruntwork.io/a-comprehensive-guide-to-terraform-b3d32832baca
        -   Set proper region in `terraform/environment/terraform.tfvars`
        -   Replace all required `##replace##` variables in all `terraform.tfvars` files, both in main env and env-specific
        -   Set AWS credentials in environment (Get it from your terraform user, set `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`).
        -   Create `secrets.tfvars` file for each environment. There you can place all env-specific variables that you don't want to keep in repo.
        -   **For running commands ALWAYS use terragrunt!!!!** It handles locking and managing remote state on aws, so tool may be used in team.
            Commands have to be run in environment directory, for example `environments/staging`.
            -   `terragrunt plan` for showing changes
            -   `terragrunt apply` for committing changes
            -   `terragrunt destroy` for destroying env

    -   After creating application via terraform, ElasticBeanstalk creates a S3 bucket, you need to copy it's name and insert it into `deployment.py` file.

        -   You need to fill all variables marked as `##replace##`.
        -   Fill `##replace##` in `config/letsencrypt/config.ini`.

    -   HTTPS certificates are generated automatically for domain that you will provide in terraform vars.
        Remember that Domain must point to server at the moment of deploy, because there may happen that letsencrypt won't be able to validate server and will temporarily block possibility of generating certs.

    -   Application environment must correspond to branch name, so if we want to deploy staging/live, we need to use branches with same names.

-   Replace required variables in `backend/deployment.py`

<br />

## Navigate

[Return to main README page](README.md)

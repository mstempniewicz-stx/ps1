module "network" {
  source = "../network"
  prefix = "${var.prefix}"
}

module "main_db" {
  source      = "../db"
  prefix      = "${var.prefix}"
  vpc_id      = "${module.network.vpc_id}"
  db_subnets  = "${join(",", "${module.network.subnets}")}"
  db_password = "${var.db_password}"
}

resource "aws_elastic_beanstalk_application" "web" {
  name        = "${var.prefix}-web"
  description = "${var.prefix}-web"
}

resource "aws_elastic_beanstalk_environment" "web" {
  name                = "${var.prefix}-web"
  application         = "${aws_elastic_beanstalk_application.web.name}"
  solution_stack_name = "64bit Amazon Linux 2017.09 v2.9.2 running Multi-container Docker 17.12.0-ce (Generic)"
  tier                = "WebServer"

  ###############
  # Network
  ###############
  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = "${module.network.vpc_id}"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = "${join(",", module.network.subnets)}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:healthreporting:system"
    name      = "SystemType"
    value     = "enhanced"
  }

  setting {
    namespace = "aws:elasticbeanstalk:healthreporting:system"
    name      = "HealthCheckSuccessThreshold"
    value     = "Warning"
  }

  ###############
  # launchconfig
  ###############
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = "${module.main_db.dbaccess_sg_id},${module.network.web_access_sg_id},${module.network.ssh_access_sg_id},${aws_security_group.redisaccess.id}"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t2.micro"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "EC2KeyName"
    value     = "${var.key_pair_name}"
  }

  ###############
  # ENV variables
  ###############
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "ENVIRONMENT"
    value     = "${var.application_environment}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_HOST"
    value     = "${element(split(":", module.main_db.db_endpoint), 0)}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_USER"
    value     = "${module.main_db.db_username}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_NAME"
    value     = "${module.main_db.db_name}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_PASS"
    value     = "${var.db_password}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DB_PORT"
    value     = "${module.main_db.db_port}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "REDIS_URI"
    value     = "${aws_elasticache_replication_group.main.primary_endpoint_address}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DOMAIN"
    value     = "${var.domain_name}"
  }

  ########
  # Deploy
  ########
  setting {
    namespace = "aws:elasticbeanstalk:command"
    name      = "BatchSizeType"
    value     = "Fixed"
  }

  setting {
    namespace = "aws:elasticbeanstalk:command"
    name      = "BatchSize"
    value     = "1"
  }

  setting {
    namespace = "aws:elasticbeanstalk:command"
    name      = "DeploymentPolicy"
    value     = "Rolling"
  }

  tags {
    Env = "${var.prefix}"
  }
}

resource "aws_security_group" "redisaccess" {
  name        = "${var.prefix}-redisaccess"
  description = "Allow connecting to ${var.prefix} redis"
  vpc_id      = "${module.network.vpc_id}"

  tags {
    Name = "${var.prefix}-redisaccess"
    Env  = "${var.prefix}"
  }
}

resource "aws_security_group" "redis" {
  name        = "${var.prefix}-redis"
  description = "Allow inbound traffic to redis"
  vpc_id      = "${module.network.vpc_id}"

  tags {
    Name = "${var.prefix}-redis"
    Env  = "${var.prefix}"
  }

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "TCP"
    security_groups = ["${aws_security_group.redisaccess.id}"]
  }

  tags {
    Name = "${var.prefix}-redis"
    Env  = "${var.prefix}"
  }
}

resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.prefix}-main"
  subnet_ids = ["${module.network.subnets}"]
}

resource "aws_elasticache_replication_group" "main" {
  replication_group_id          = "${var.prefix}-main"
  replication_group_description = "${var.prefix}-main"
  engine                        = "redis"
  node_type                     = "cache.t2.micro"
  number_cache_clusters         = 1
  subnet_group_name             = "${aws_elasticache_subnet_group.main.name}"
  port                          = 6379
  security_group_ids = ["${aws_security_group.redis.id}"]

  tags {
    Name = "${var.prefix}-main"
    Env  = "${var.prefix}"
  }
}

module "primary_domain" {
  source      = "../dns"
  prefix      = "${var.prefix}-primary"
  domain_name = "${var.domain_name}"
  app_cname   = "${aws_elastic_beanstalk_environment.web.cname}"
}

import os
import time
import zipfile
from io import BytesIO
from pprint import pformat

import boto3
from botocore.exceptions import ClientError

DOCKER_CONFS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docker"
)
AWS_REGION = "eu-west-1"

# Names for docker container and image on EB
DOCKER_NAME = "##replace##"

# registry/user, same as in codeship-steps,
# Example: 1111.dkr.ecr.eu-west-1.amazonaws.com/stx
DOCKER_HUB_ACCOUNT = "##replace##"

# name of image in registry, same as in codeship-steps, Example: web
DOCKER_IMAGE = "##replace##"

# There 2 values are formatted with env name, so leave empty {} for it
# Example stx-{}-web, where {} is replace with staging, live etc.
# In most cases these values can be the same
# This is name of application and environment in elastic beanstalk, so keep it same
# like in terraform
EBS_APP_NAME = "##replace##"
EBS_ENV_NAME = "##replace##"

# Bucket where zip with application files are uploaded
# You can get it after you create environment in EBS. Just open S3 and find newly
# created bucket
# Example: elasticbeanstalk-eu-west-1-1111111111
APP_BUCKET = "##replace##"


def upload_version_to_s3(version, source_folder, s3_file_name, bucket_name):
    s3 = boto3.resource("s3")
    print("version - ", version)
    source_folder.seek(0)
    res = s3.Object(bucket_name.lower(), s3_file_name).put(Body=source_folder)
    print("uploaded")
    return res


def create_application_version(app_name, version, bucket_name, s3_file_name):
    eb = boto3.client("elasticbeanstalk", region_name=AWS_REGION)
    try:
        eb.create_application_version(
            ApplicationName=app_name,
            VersionLabel=version,
            Description=version,
            SourceBundle={"S3Bucket": bucket_name, "S3Key": s3_file_name},
            AutoCreateApplication=True,
            Process=True,
        )
    except ClientError as err:
        if "already exists" in err.response["Error"]["Message"]:
            print("already exist")
            pass
        else:
            print("ERROR - ", err)


def update_environment(version, application_name, environment_name):
    eb = boto3.client("elasticbeanstalk", region_name=AWS_REGION)
    status = ""
    while status != "PROCESSED":
        status = eb.describe_application_versions(
            ApplicationName=application_name, VersionLabels=[version]
        )["ApplicationVersions"][0]["Status"]
        print("application not updated yet", status)
        time.sleep(10)

        print("application details:", application_name, environment_name, version)
    res = eb.update_environment(
        ApplicationName=application_name,
        EnvironmentName=environment_name,
        VersionLabel=version,
    )["Status"]

    print("status after update is - ", pformat(res))
    while res != "Ready":
        env = eb.describe_environments(
            ApplicationName=application_name, EnvironmentNames=[environment_name]
        )["Environments"][0]
        try:
            res = env["Status"]
        except (KeyError, IndexError):
            res = "Waiting!!"
        print(f"Status: {res}")
        time.sleep(5)


def zip_folder(source_folder):
    with zipfile.ZipFile(source_folder, "w", zipfile.ZIP_DEFLATED) as zipf:
        # ziph is zipfile handle
        base_path = "./tmp/package"

        for root, dirs, files in os.walk(base_path):
            for file in files:
                path = os.path.join(root, file)
                zipf.write(path, path.replace(base_path, ""))


def get_commit_id():
    try:
        commit_id = os.environ.get("CI_COMMIT_ID")
    except TypeError:
        commit_id = (os.popen("git rev-parse HEAD").read()).strip()
    if not commit_id:
        commit_id = (os.popen("git rev-parse HEAD").read()).strip()

    return commit_id


def get_branch_id():
    branch_id = None

    try:
        branch_id = os.environ.get("CI_BRANCH")
    except TypeError:
        pass

    if not branch_id:
        branch_id = (os.popen("git branch | grep \\* | cut -d ' ' -f2").read()).strip()

    if not branch_id:
        branch_id = "test"

    return branch_id


def generate_tag():
    tag = f"{get_branch_id()}-{get_commit_id()}"
    print(f"generated tag: {tag}")
    return tag


def clear_tmp():
    os.system("rm -rf ./tmp && mkdir -p tmp/package")


def prepare_dockerrun(tag):
    print("Updating Dockerrun with tag - {}".format(tag))

    clear_tmp()
    tmp_path = os.path.join("tmp", "package")

    replace_file_content(
        os.path.join(DOCKER_CONFS_DIR, "Dockerrun.aws.json"),
        os.path.join(tmp_path, "Dockerrun.aws.json"),
        {
            "docker_name": DOCKER_NAME,
            "dockerhub_account": DOCKER_HUB_ACCOUNT,
            "docker_image": DOCKER_IMAGE,
            "version_tag": tag,
        },
    )

    # Uncomment this line if you want to add .ebextensions
    # copy_tree(
    #   os.path.join(DOCKER_CONFS_DIR}, '.ebextensions'), f'./tmp/package/.ebextensions'
    # )


def replace_file_content(src, dst, args):
    with open(src, "r") as template_f:
        content = template_f.read() % args

    with open(dst, "w+") as target_f:
        target_f.write(content)
        target_f.truncate()


def get_eb_application():
    """Use this to get application and environment for AWS."""
    branch = get_branch_id()

    return (EBS_APP_NAME.format(branch), EBS_ENV_NAME.format(branch))


def deploy():
    app_name, env_name = get_eb_application()
    tag = generate_tag()
    version = f"{DOCKER_IMAGE}-{tag}"
    prepare_dockerrun(tag)
    s3_file_name = f"{app_name}/{version}.zip"
    source_folder = BytesIO()

    zip_folder(source_folder)
    upload_version_to_s3(version, source_folder, s3_file_name, APP_BUCKET)
    create_application_version(app_name, version, APP_BUCKET, s3_file_name)
    update_environment(version, app_name, env_name)


if __name__ == "__main__":
    deploy()

from aws_cdk import (
    Stack,
    aws_s3_assets as s3_assets,
    aws_elasticbeanstalk as eb,
    aws_iam as iam,
)
from constructs import Construct

class FlaskEbsStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Upload app.zip as an S3 asset
        app_asset = s3_assets.Asset(self, "FlaskAppZip", path="cdk/app.zip")

        # Elastic Beanstalk application
        app = eb.CfnApplication(self, "FlaskApp", application_name="FlaskEbsApp")

        # Application version (points to the zip in S3)
        app_version = eb.CfnApplicationVersion(self, "AppVersion",
            application_name=app.application_name,
            source_bundle=eb.CfnApplicationVersion.SourceBundleProperty(
                s3_bucket=app_asset.s3_bucket_name,
                s3_key=app_asset.s3_object_key
            )
        )

        # IAM role for EC2 instances
        role = iam.Role(self, "EbsEC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSElasticBeanstalkWebTier"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))

        instance_profile = iam.CfnInstanceProfile(self, "InstanceProfile",
            roles=[role.role_name]
        )

        # Elastic Beanstalk environment
        env = eb.CfnEnvironment(self, "FlaskEnv",
            environment_name="FlaskEbsEnv",
            application_name=app.application_name,
            solution_stack_name="64bit Amazon Linux 2 v3.5.4 running Python 3.8",
            option_settings=[
                eb.CfnEnvironment.OptionSettingProperty(
                    namespace="aws:autoscaling:launchconfiguration",
                    option_name="IamInstanceProfile",
                    value=instance_profile.ref
                ),
                eb.CfnEnvironment.OptionSettingProperty(
                    namespace="aws:elasticbeanstalk:application:environment",
                    option_name="FLASK_ENV",
                    value="production"
                )
            ],
            version_label=app_version.ref
        )

        app_version.add_dependency(app)
        env.add_dependency(app_version)

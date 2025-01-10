terraform {
  required_version = ">= 0.12"

  backend "s3" {
    bucket = "shardul-ci-cd-tf-backend"
    key    = "state/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

# Random ID for dynamic bucket naming
resource "random_id" "unique_id" {
  byte_length = 8
}

# CloudFormation Stack to create an S3 bucket
resource "aws_cloudformation_stack" "s3_bucket" {
  name          = "ExampleS3BucketStack"
  template_body = file("${path.module}/templatefile.yaml")

  parameters = {
    BucketName = "example-unique-bucket-${random_id.unique_id.hex}"
  }

  tags = {
    Name        = "ExampleS3Bucket"
    Environment = "Dev"
  }
}


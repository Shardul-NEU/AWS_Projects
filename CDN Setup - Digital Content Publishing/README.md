# Setting Up a Content Delivery Network (CDN) with Amazon CloudFront and S3

## Overview

This repository provides a guide for setting up a Content Delivery Network (CDN) using Amazon CloudFront and Amazon S3. A CDN improves the performance of your web applications by delivering content quickly to users worldwide. This guide walks you through configuring S3 buckets and CloudFront distributions to serve your content efficiently.

## Key Components

### Amazon S3 Buckets

Amazon S3 (Simple Storage Service) is used to store and retrieve your content. S3 provides scalable storage solutions and supports bucket policies for fine-grained access control.

### Amazon CloudFront

Amazon CloudFront is a CDN that delivers your content with low latency and high transfer speeds. It uses a global network of edge locations to cache copies of your content close to your users.

## Setup Guide

### 1. Setting Up Amazon S3 Buckets

1. **Create the Buckets**
   - Create two S3 buckets if you’re using separate environments for Production and Staging. Ensure that the bucket names are distinct.
   - Example:
     - Production Bucket: `cdn-production-bucket`
     - Staging Bucket: `cdn-staging-bucket`

2. **Disable ACLs**
   - By default, disabling ACLs assigns the bucket owner ownership of all objects within the bucket and the ability to define bucket policies to manage access.

3. **Edit the Bucket Policy**
   - Add the following policy to allow necessary actions for the CloudFront origin access identity:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "AWS": "arn:aws:iam::cloudfront-origin-access-identity"
           },
           "Action": [
             "s3:GetObject",
             "s3:PutObject"
           ],
           "Resource": "arn:aws:s3:::cdn-production-bucket/*"
         }
       ]
     }
     ```

4. **Verify the S3 Buckets**
   - Use a verification file to validate each S3 bucket.

### 2. Setting Up Amazon CloudFront

1. **Create an Origin Access Identity (OAI)**
   - In CloudFront, create an OAI and note the Amazon S3 canonical User ID.
     - Example OAI:
       - ID: `E1JXAX1XN7VB84`
       - Name: `cdn-oai-prod`

2. **Create Web Distributions**
   - Create the necessary CloudFront distributions for Production and Staging environments.
   - Example Distribution Settings:
     - Origin Domain Name: S3 bucket for either Production or Staging
     - Restrict Bucket Access: Yes
     - Origin Access Identity: Use the OAI created previously
     - Grant Read Permissions: No (update permissions manually)

### 3. CloudFront Usage Logging

1. **Enable Usage Logging**
   - Navigate to AWS CloudFront and select the distribution.
   - Click `Edit` and turn on logging, specifying a bucket for logging data.
   - Example Log Bucket: `cdn-logging-bucket`
   - Set a Log Prefix, e.g., `logging/`.

2. **Configure Lambda Function for Logging**
   - Create and configure a Lambda function to automatically grant read permissions for CloudFront logs.
   - Example Lambda Policy:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "logs:CreateLogGroup",
             "logs:CreateLogStream",
             "logs:PutLogEvents"
           ],
           "Resource": "arn:aws:logs:*:*:*"
         },
         {
           "Effect": "Allow",
           "Action": [
             "s3:GetObjectAcl",
             "s3:GetBucketAcl",
             "s3:PutObjectAcl"
           ],
           "Resource": [
             "arn:aws:s3:::cdn-logging-bucket/*",
             "arn:aws:s3:::cdn-logging-bucket"
           ]
         }
       ]
     }
     ```

3. **Deploy the Lambda Function**
   - Configure triggers for the Lambda function to grant read permissions for logs.
   - Example Lambda Function: `cdn-logging-lambda`
   - Code and Trigger:
     - Code: Upload your Lambda function code.
     - Trigger: S3 Bucket: `cdn-logging-bucket`

## Advantages

- **Scalability:** Seamlessly scale to accommodate large volumes of content.
- **Performance:** Reduce latency and improve load times for global users.
- **Automation:** Use Lambda functions to automate permission management and log processing.

## Code

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront-origin-access-identity"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::cdn-production-bucket/*"
    }
  ]
}

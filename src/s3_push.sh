#!/usr/bin/env bash
set -e

aws s3 rm s3://$S3_BUCKET --recursive
aws s3 sync front_end/templates/ s3://$S3_BUCKET/

echo "pushed files to S3 bucket"
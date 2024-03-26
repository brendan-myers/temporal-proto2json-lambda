# Temporal Proto to JSON Lambda

An AWS Lambda function for converting [Temporal Workflow History exports](https://docs.temporal.io/cloud/export) from protobuf to JSON.

## Prerequisites

* 2x S3 buckets
    * One bucket configured to receive Workflow Histories from Temporal (protobuf). To test the Lambda function, this should already have at least one exported workflow history.
    * The other is the target for this function; it's where the converted JSON will be sent.
* An IAM role that Lambda can assume when running your function. This role needs the following policy;

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:s3:::REPLACE_WITH_SOURCE_BUCKET/*",
                "arn:aws:logs:*:*:*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::REPLACE_WITH_TARGET_BUCKET/*"
        }
    ]
}
```

## Lambda Configuration

* Runtime: `Python 3.x`
* Architecture: `arm64`
* Execution Role: Use the role that has the policy from the prereqs attached.

Once the function is created;

* Add an S3 trigger
    * The bucket will be your SOURCE bucket
    * Prefix: `temporal-workflow-history/`
* Add an environment variable specifying the target bucket. NOTE: just use the bucket name, don't prefix it with `s3://`.
    * `S3_TARGET_BUCKET` - 'bucket_name'


## Package the function and upload it to Lambda

* Create `lambda_funciton.zip`;

```
chmod +x create_zip.sh
./create_zip.sh
```

* In the `code` tab in Lambda, select `Upload from > .zip file` and upload the zip.
* To test, select the `s3-put` template on the `test` tab in Lambda. Modify `s3:bucket:name` and `s3:object:key` so that they use the real location of a workflow history export proto in your source bucket.


## TODO
* Turn this into a CF/TF script
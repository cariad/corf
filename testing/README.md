# Testing

## `sample_filesystem`

`sample_filesystem` is used by unit tests to assert that a configuration across multiple files and directories is merged with the correct precedence.

## `sample_project`

`sample_project` contains:

- A CloudFormation template for deploying a sample CodeArtifact domain and repository, and an IAM user with permission to pull packages.
- A `Pipfile` template for pulling packages from the CodeArtifact repository.

To set up the AWS infrastructure for testing the CLI:

1. Deploy the CloudFormation template.
1. Create an access key pair for the IAM user created in that stack, and set the values as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` secrets in the GitHub project.

The CI pipeline will authenticate as that user and assert that it's able to use `corf` to generate an authorisation token and pull from the repository.

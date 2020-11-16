# corf: A CodeArtifact Orthoriser

`corf` is an AWS CodeArtifact orthorisation… uh I mean _authorisation_ helper for `pipenv` and any other command line tools that read CodeArtifact authorisation tokens as environment variables.

## Problem

Let's say you have a `Pipfile` that describes an AWS CodeArtifact repository as a source:

```text
[[source]]
name = "freyda-pypackages"
url = "https://aws:$CODEARTIFACT_AUTH_TOKEN@starkindustries-012345678901.d.codeartifact.us-east-1.amazonaws.com/pypi/project-ultron/simple"
verify_ssl = true
```

How do you set that `CODEARTIFACT_AUTH_TOKEN` environment variable?

Sure, if you develop in Bash then you could run the `aws` command line to refresh your token twice a day:

```bash
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token --domain starkindustries --domain-owner 012345678901 --query authorizationToken --output text --region us-east-1)
```

And--sure--there are ways of simplifying and automating it. But what if you're supporting developers across a range of operating systems and shells? What if you're supporting developers across a range of patience to muck around with shell internals to automate their lives? What if you spin up a fresh virtual machine to play around in, and you just want to authenticate in an unconfigured shell and no recollection of the `aws` command to run?

That's where `cauth` comes in. `cauth` replaces all that setup, mental load and shell-specificity with:

```bash
cauth pipenv install
```

## Installation

```bash
pip install corf
```

## Project setup

### Simple example

Create a file named `.cauth.yml` inside your project directory like this:

```yaml
variables:
  - account: <CodeArtifact repository account ID>
    domain:  <CodeArtifact repository domain>
    name:    <Environment variable>
    region:  <CodeArtifact repository region>
```

For example, for any repository in the "starkindustries" domain in "us-east-1" in AWS account "012345678901", you could create this `.cauth.yml` to generate authorisation tokens into the "CODEARTIFACT_AUTH_TOKEN" environment variable:

```yaml
variables:
  - account: "012345678901"
    domain:  starkindustries
    name:    CODEARTIFACT_AUTH_TOKEN
    region:  us-east-1
```

To invoke `pipenv` with a fresh authorisation token:

```bash
cauth pipenv install
```

### Profiles and local configuration files

If your AWS credentials are in a named profile then you have three options:

First, you can pass the profile to `cauth` on the command line:

```bash
cauth --profile corporate pipenv install
```

Note that `--profile` _must_ be the first argument.

Second, _could_ add it into `.cauth.yml`:

```yaml
variables:
  - account: "012345678901"
    domain:  starkindustries
    name:    CODEARTIFACT_AUTH_TOKEN
    region:  us-east-1
    profile: corporate
```

This isn't typically recommended, since `.cauth.yml` is shared with your team via source control and they might use different named profiles (or none at all).

So, the third option is to copy `.cauth.yml` into `.cauth.user.yml`, put the named profile into that, and do not commit `.cauth.user.yml` to source control.

# Should .cauth.yml files be committed to source control?

`.cauth.yml`, yes.

`.cauth.user.yml`, no.

## Testing

```bash
./lint.sh && ./coverage.sh && ./build.sh
```

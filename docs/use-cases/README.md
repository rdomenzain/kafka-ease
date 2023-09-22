# CI/CD

This tool has several uses. Either for manual execution via the command line or even using the library in another Python project.

But the idea is to automate these tasks, CI/CD helps automate them. A repository on GitHub or Gitlab with .yaml or .json configuration files is a real use case.

You can define rules for the execution of these tasks using merge requests.

1. Open Merge Request: File Validation
2. Merge: Apply changes to Kafka

!!! info "Note" 
    The following examples are for GitLab CI/CD and GitHub Actions. But you can use any CI/CD tool.

## GitLab CI/CD

```yml title=".gitlab-ci.yml"
stages:
  - validate
  - sync

kafka-validate:
  stage: validate
  image: python:3.9
  script:
    - pip install kafka-ease
    - kafka-ease apply -f ./kafka-init.yml --only-validate
  rules:
    - if: $CI_MERGE_REQUEST_ID
      changes:
        - ./**/*.{yml}

kafka-sync:
  stage: sync
  image: python:3.9
  script:
    - pip install kafka-ease
    - kafka-ease apply -f ./kafka-init.yml
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      changes:
        - ./**/*.{yml}
```

## GitHub Actions

```yml title=".github/workflows/main.yml"
name: Kafka CI/CD

on:
  pull_request:
    paths:
      - '**/*.yml'
  push:
    branches:
      - main # Change this to your GitHub default branch name if different

jobs:
  kafka-validate:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9

    - name: Install kafka-ease
      run: pip install kafka-ease

    - name: Validate Kafka configuration
      run: kafka-ease apply -f ./kafka-init.yml --only-validate

    if: github.event_name == 'pull_request'

  kafka-sync:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9

    - name: Install kafka-ease
      run: pip install kafka-ease

    - name: Sync Kafka configuration
      run: kafka-ease apply -f ./kafka-init.yml

    if: github.event_name == 'push' && github.ref == 'refs/heads/main' # Adjust the branch here as well
```

!!! warning "Warning"
    These examples use environment variables for greater security.

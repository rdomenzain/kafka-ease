# Kafka Ease

Automating the creation of topics and ACLs is a common task for Kafka administrators. This repository contains a set of utilities to automate these tasks.

- Create a topic with a given number of partitions and replication factor
- Create ACLs for a given topic

![coverage badge](./coverage.svg)

[![CI](https://github.com/rdomenzain/kafka-ease/actions/workflows/main.yml/badge.svg)](https://github.com/rdomenzain/kafka-ease/actions/workflows/main.yml)

See the [documentation](https://rdomenzain.github.io/kafka-ease/) for more information.

## Contents

- [Kafka Ease](#kafka-ease)
  - [Contents](#contents)
  - [Getting started](#getting-started)
    - [Installation](#installation)
      - [requirements.txt](#requirementstxt)
      - [Pip install](#pip-install)
  - [How to use](#how-to-use)
    - [File format](#file-format)
    - [Validate configuration](#validate-configuration)
    - [Apply configuration](#apply-configuration)
    - [Help](#help)
  - [Changelog](#changelog)

## Getting started

### Installation

#### requirements.txt

To install the library from the GitLab package registry, write the following lines in the file `requirements.txt`:

```text
kafka-ease==[VERSION]
```

#### Pip install

To install the library, run the following command:

```bash
pip install kafka-ease==[VERSION]
```

Check [PEP 440](https://www.python.org/dev/peps/pep-0440/) for version schemes and version specifiers.

## How to use

### File format

The file format is YAML or JSON. The file must contain a list of topics and a list of ACLs.

```yaml
# acl.yaml
topics:
  - name: topic.name
    num_partitions: 1
    replication_factor: 1
    cleanup_policy: delete
    retention_days: 7

acls:
  - resource_type: TOPIC
    resource_name: topic.name
    principal: User:kafka-user
    host: "*"
    operation: READ
    permission_type: ALLOW
    pattern_type: LITERAL
```

```json
{
  "topics": [
    {
      "name": "topic.name",
      "num_partitions": 1,
      "replication_factor": 1,
      "cleanup_policy": "delete",
      "retention_days": 7
    }
  ],
  "acls": [
    {
      "resource_type": "TOPIC",
      "resource_name": "topic.name",
      "principal": "User:kafka-user",
      "host": "*",
      "operation": "READ",
      "permission_type": "ALLOW",
      "pattern_type": "LITERAL"
    }
  ]
}
```

- Topics
  - **name**: Topic name
  - **num_partitions**: Number of partitions
  - **replication_factor**: Replication factor
  - **cleanup_policy**: Cleanup policy (`delete`, `compact`)
  - **retention_days**: Delete retention days

- ACLs
  - **resource_type**: Resource type (`UNKNOWN`, `ANY`, `CLUSTER`, `TOPIC`, `DELEGATION_TOKEN`, `GROUP`, `TRANSACTIONAL_ID`)
  - **resource_name**: Resource name
  - **principal**: Principal (`User:`, `Group:`)
  - **host**: Host (`*`)
  - **operation**: Operation (`ANY`, `ALL`, `READ`, `WRITE`, `CREATE`, `DELETE`, `ALTER`, `DESCRIBE`, `CLUSTER_ACTION`, `DESCRIBE_CONFIGS`, `ALTER_CONFIGS`, `IDEMPOTENT_WRITE`)
  - **permission_type**: Permission type (`ANY`, `DENY`, `ALLOW`)
  - **pattern_type**: Pattern type (`ANY`, `MATCH`, `LITERAL`, `PREFIXED`)

### Validate configuration

```shell
kafka-ease apply -f acl.yaml --only-validate
```

Expected output:

```text
Validating file acl.yaml...
File: acl.yaml
YAML file detected
2 topics found.
2 ACLs found.
File acl.yaml is valid.
```

### Apply configuration

```shell
kafka-ease apply -f acl.yaml \
  --kafka-brokers kafka:9093 \
  --security-protocol SASL_PLAINTEXT \ 
  --sasl-mechanism SCRAM-SHA-256 \
  --sasl-username kafka-admin \
  --sasl-password SECRET
```

Expected output:

```text
Applying file...
Kafka brokers: kafka:9093
Security protocol: SASL_PLAINTEXT
SASL mechanism: SCRAM-SHA-256
SASL username: kafka-admin
SASL password: ***************
File: acl.yaml
YAML file detected
1 topics found.
1 ACLs found.
Topic topic.name updated
Removing old ACLs 3
ACL User:kafka-user synced
File synced successfully.
```

### Help

```shell
kafka-ease apply --help
```

Expected output:

```text
Usage: kafka-ease apply [OPTIONS]

  Apply configuration file with topics and ACL to Kafka.

Options:
  --kafka-brokers TEXT            Kafka server to connect to use.
  --security-protocol [PLAINTEXT|SASL_PLAINTEXT]
                                  Kafka Security protocol to use.
  --sasl-mechanism [PLAIN|SCRAM-SHA-256|SCRAM-SHA-512]
                                  SASL mechanism to use.
  --sasl-username TEXT            SASL username to use.
  --sasl-password TEXT            SASL password to use.
  -f, --file TEXT                 File path to validate
  --only-validate                 Only validate the file
  --help                          Show this message and exit.
```

## Changelog

- 1.0.0 (2023-09-20)
  > Initial release of Kafka Ease
- 1.0.1 (2023-09-20)
  > Fix packaging error
- 1.0.2 (2023-09-20)
  > Fix minor bugs

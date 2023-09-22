## Validate configuration

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

## Apply configuration

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

## Help

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

## Use environment variables

Use environment variables to avoid passing the same parameters every time.

```shell
export KAFKA_BROKERS=kafka:9093
export KAFKA_SECURITY_PROTOCOL=SASL_PLAINTEXT
export KAFKA_SASL_MECHANISM=SCRAM-SHA-256
export KAFKA_SASL_USERNAME=kafka-admin
export KAFKA_SASL_PASSWORD=SECRET

kafka-ease apply -f acl.yaml
```

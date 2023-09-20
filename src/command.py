from typing import List

from click import echo
from kafka.admin import NewTopic, ACL

from .read_file import ReadFile
from .validator import Validator
from .kafka_handler import KafkaHandler


class Command:
    """This class is responsible for running the command."""

    def __init__(
        self,
        kafka_brokers: str,
        security_protocol: str,
        sasl_mechanism: str,
        sasl_username: str,
        sasl_password: str,
        file: str,
        only_validate: bool,
    ):
        """
        Create a Command instance.
        Args:
            kafka_brokers: Kafka brokers
            security_protocol: Security protocol
            sasl_mechanism: SASL mechanism
            sasl_username: SASL username
            sasl_password: SASL password
            file: File to read
            only_validate: Only validate file
        """
        self.kafka_brokers: str = kafka_brokers
        self.security_protocol: str = security_protocol
        self.sasl_mechanism: str = sasl_mechanism
        self.sasl_username: str = sasl_username
        self.sasl_password: str = sasl_password
        self.file: str = file
        self.only_validate: bool = only_validate

    def run(self):
        """Run the command."""
        if self.only_validate:
            echo(f"Validating file {self.file}...")
        else:
            echo("Applying file...")

            echo(f"Kafka brokers: {self.kafka_brokers}")
            echo(f"Security protocol: {self.security_protocol}")
            echo(f"SASL mechanism: {self.sasl_mechanism}")
            echo(f"SASL username: {self.sasl_username}")
            echo(
                f"SASL password: {self.sasl_password.replace(self.sasl_password, '*' * len(self.sasl_password))}"
            )

        if self.file is None:
            echo("File not found.")
            return

        echo(f"File: {self.file}")
        read_file = ReadFile(self.file)
        data = read_file.read()
        # Validate file
        validator = Validator()
        topics: List[NewTopic] = validator.check_topics(data=data)
        acls: List[ACL] = validator.check_acls(data=data)

        echo(f"{len(topics)} topics found.")
        echo(f"{len(acls)} ACLs found.")

        if self.only_validate:
            echo(f"File {self.file} is valid.")
            return

        if self.kafka_brokers is None:
            echo("Kafka brokers not found.")
            return

        if self.sasl_username is None:
            echo("SASL username not found.")
            return

        if self.sasl_password == "" or self.sasl_password is None:  # nosec
            echo("SASL password not found.")
            return

        kafka: KafkaHandler = KafkaHandler(
            kafka_brokers=self.kafka_brokers,
            security_protocol=self.security_protocol,
            sasl_mechanism=self.sasl_mechanism,
            sasl_username=self.sasl_username,
            sasl_password=self.sasl_password,
        )

        # Create topics
        if len(topics) > 0:
            kafka.create_topics(topics=topics)

        # Create ACLs
        if len(acls) > 0:
            kafka.create_acls(acls=acls)

        kafka.close()
        echo("File synced successfully.")

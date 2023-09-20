from typing import List

from click import echo
from kafka.admin import (
    KafkaAdminClient,
    NewTopic,
    ConfigResource,
    ConfigResourceType,
    ACL,
    ACLFilter,
    ACLOperation,
    ACLPermissionType,
    ResourcePatternFilter,
    ResourceType,
    ACLResourcePatternType,
)


class KafkaHandler:
    """This class is responsible for handling Kafka topics and ACLs."""

    def __init__(
        self,
        kafka_brokers: str,
        security_protocol: str,
        sasl_mechanism: str,
        sasl_username: str,
        sasl_password: str,
    ):
        """Create a KafkaTopic instance.
        Args:
            kafka_brokers (str): Kafka brokers
            security_protocol (str): Security protocol
            sasl_mechanism (str): SASL mechanism
            sasl_username (str): SASL username
            sasl_password (str): SASL password
        """
        self.admin_client: KafkaAdminClient = KafkaAdminClient(
            bootstrap_servers=kafka_brokers,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_username,
            sasl_plain_password=sasl_password,
        )

    def create_topics(self, topics: List[NewTopic]):
        """Create topics.
        Args:
            topics (List[NewTopic]): List of topics to create
        """
        topic_metadata = self.admin_client.list_topics()
        for topic in topics:
            if topic.name in topic_metadata:
                fs = self.admin_client.alter_configs(
                    [
                        ConfigResource(
                            resource_type=ConfigResourceType.TOPIC,
                            name=topic.name,
                            configs=topic.topic_configs,
                        )
                    ]
                )
                if fs:
                    echo(f"Topic {topic.name} updated")
            else:
                fs = self.admin_client.create_topics([topic])
                if fs:
                    echo(f"Topic {topic.name} created")

    def create_acls(self, acls: List[ACL]):
        """Create new ACLs and remove old ones.
        Args:
            acls (List[ACL]): List of ACLs to create
        """
        filter_acls: ACLFilter = ACLFilter(
            principal=None,
            host=None,
            operation=ACLOperation.ANY,
            permission_type=ACLPermissionType.ANY,
            resource_pattern=ResourcePatternFilter(
                resource_type=ResourceType.ANY,
                resource_name=None,
                pattern_type=ACLResourcePatternType.ANY,
            ),
        )
        kafka_acls = self.admin_client.describe_acls(acl_filter=filter_acls)

        for acl in acls:
            filter_acls = ACLFilter(
                principal=acl.principal,
                host=acl.host,
                operation=acl.operation,
                permission_type=acl.permission_type,
                resource_pattern=ResourcePatternFilter(
                    resource_type=acl.resource_pattern.resource_type,
                    resource_name=acl.resource_pattern.resource_name,
                    pattern_type=acl.resource_pattern.pattern_type,
                ),
            )
            file_acls = self.admin_client.describe_acls(acl_filter=filter_acls)
            if len(file_acls[0]) > 0:
                echo(f"ACL {acl.principal} already exists")
            else:
                self.admin_client.create_acls([acl])
                echo(f"ACL {acl.principal} created")

            for kafka_acl in kafka_acls[0]:
                if kafka_acl == acl:
                    kafka_acls[0].remove(kafka_acl)

        for kafka_acl in kafka_acls[0]:
            self.admin_client.delete_acls([kafka_acl])
            echo(f"ACL {kafka_acl.principal} removed")

    def close(self):
        """Close the KafkaAdminClient."""
        self.admin_client.close()

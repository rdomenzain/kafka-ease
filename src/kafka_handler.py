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
        """Create ACLs and update if exists.
        Args:
            acls (List[ACL]): List of ACLs to create
        """
        filter_acls = ACLFilter(
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
        acls_metadata = self.admin_client.describe_acls(acl_filter=filter_acls)
        echo(f"Removing old ACLs {len(acls_metadata[0])}")
        for acl in acls_metadata[0]:
            self.admin_client.delete_acls([acl])

        for acl in acls:
            self.admin_client.create_acls([acl])
            echo(f"ACL {acl.principal} synced")

    def close(self):
        """Close the KafkaAdminClient."""
        self.admin_client.close()

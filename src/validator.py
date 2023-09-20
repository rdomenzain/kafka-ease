from typing import Dict, List

from click import echo
from kafka.admin import (
    NewTopic,
    ACL,
    ResourcePattern,
    ResourceType,
    ACLPermissionType,
    ACLOperation,
    ACLResourcePatternType,
)


class Validator:
    """ This class validates the configuration file. """
    @staticmethod
    def check_topics(data: Dict) -> List[NewTopic]:
        """Check topics, return a list of NewTopic objects.
        Args:
            data (Dict): Data from file
        Returns:
            List[NewTopic]: List of NewTopic objects
        """
        topics: List[NewTopic] = []
        topic_name: str
        num_partitions: int
        replication_factor: int
        cleanup_policy: str
        retention_ms: int
        if not data.get("topics", []):
            echo("No topics found")

        for topic in data.get("topics", []):

            if not topic.get("name", None):
                raise Exception("Topic name is required")
            else:
                topic_name = topic["name"]

            if not topic.get("num_partitions", None):
                echo(
                    f"{topic_name}: Topic num_partitions is required, "
                    f"using default value 1"
                )
                num_partitions = 1
            else:
                num_partitions = topic["num_partitions"]

            if not topic.get("replication_factor", None):
                replication_factor = 1
                echo(
                    f"{topic_name}: Topic replication_factor is required, "
                    f"using default value 1"
                )
            else:
                replication_factor = topic["replication_factor"]

            if not topic.get("cleanup_policy", None):
                cleanup_policy = "delete"
                echo(
                    f"{topic_name}: Topic cleanup_policy is required, "
                    f"using default value 'delete'"
                )
            else:
                if topic["cleanup_policy"] not in ["delete", "compact"]:
                    raise Exception(
                        f"{topic_name}: Topic cleanup_policy must be "
                        f"'delete' or 'compact'"
                    )
                else:
                    cleanup_policy = topic["cleanup_policy"]

            if not topic.get("retention_days", None):
                retention_ms = 7 * 24 * 60 * 60 * 1000
                echo(
                    f"{topic_name}: Topic retention_days is required, "
                    f"using default value 7"
                )
            else:
                retention_ms = topic["retention_days"] * 24 * 60 * 60 * 1000

            topics.append(
                NewTopic(
                    name=topic_name,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor,
                    topic_configs={
                        "cleanup.policy": cleanup_policy,
                        "retention.ms": retention_ms,
                    },
                )
            )

        return topics

    @staticmethod
    def check_acls(data: Dict) -> List[ACL]:
        """Check acls, return a list of ACL objects.
        Args:
            data (Dict): Data from file
        Returns:
            List[ACL]: List of ACL objects
        """
        acls: List[ACL] = []
        resource_type: ResourceType
        resource_name: str
        principal: str
        host: str
        operation: ACLOperation
        permission_type: ACLPermissionType
        pattern_type: ACLResourcePatternType
        if not data.get("acls", []):
            echo("No acls found")

        for acl in data.get("acls", []):

            if not acl.get("resource_type", None):
                raise Exception("ACL resource_type is required")
            else:
                resource_type = Validator.get_enum_value(
                    enum_class=ResourceType, value=acl["resource_type"]
                )
                if not resource_type:
                    raise Exception(
                        f"Invalid resource_type: {acl['resource_type']}, "
                        f"valid values are: UNKNOWN, ANY, CLUSTER, TOPIC,"
                        f"DELEGATION_TOKEN, GROUP, TRANSACTIONAL_ID."
                    )

            if not acl.get("resource_name", None):
                raise Exception("ACL resource_name is required")
            else:
                resource_name = acl["resource_name"]

            if not acl.get("principal", None):
                raise Exception("ACL principal is required")
            else:
                principal = acl["principal"]

            if not acl.get("host", None):
                raise Exception("ACL host is required")
            else:
                host = acl["host"]

            if not acl.get("operation", None):
                raise Exception("ACL operation is required")
            else:
                operation = Validator.get_enum_value(
                    enum_class=ACLOperation, value=acl["operation"]
                )
                if not operation:
                    raise Exception(
                        f"Invalid operation: {acl['operation']}, "
                        f"valid values are: ANY, ALL, READ, WRITE, CREATE, "
                        f"DELETE, ALTER, DESCRIBE, CLUSTER_ACTION, "
                        f"DESCRIBE_CONFIGS, ALTER_CONFIGS, IDEMPOTENT_WRITE"
                    )

            if not acl.get("permission_type", None):
                raise Exception("ACL permission_type is required")
            else:
                permission_type = Validator.get_enum_value(
                    enum_class=ACLPermissionType, value=acl["permission_type"]
                )
                if not permission_type:
                    raise Exception(
                        f"Invalid permission_type: {acl['permission_type']}, "
                        f"valid values are: ANY, DENY, ALLOW"
                    )

            if not acl.get("pattern_type", None):
                pattern_type = ACLResourcePatternType.LITERAL
            else:
                pattern_type = Validator.get_enum_value(
                    enum_class=ACLResourcePatternType, value=acl["pattern_type"]
                )
                if not pattern_type:
                    raise Exception(
                        f"Invalid pattern_type: {acl['pattern_type']}, "
                        f"valid values are: ANY, MATCH, LITERAL, PREFIXED"
                    )

            acls.append(
                ACL(
                    principal=principal,
                    host=host,
                    operation=operation,
                    permission_type=permission_type,
                    resource_pattern=ResourcePattern(
                        resource_type=resource_type,
                        resource_name=resource_name,
                        pattern_type=pattern_type,
                    ),
                )
            )

        return acls

    @staticmethod
    def get_enum_value(enum_class: any, value: str) -> any:
        """Check if value is valid enum.
        Args:
            enum_class: Enum class
            value (str): Value to check
        Returns:
            any: Enum member or False
        """
        try:
            member = enum_class[value]
            return member
        except KeyError:
            return False

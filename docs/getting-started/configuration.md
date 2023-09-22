## File format

The file format is YAML or JSON. The file must contain a list of topics and a list of ACLs.

 - YAML example:

```yaml title="acl.yaml"
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

- JSON example:

```json title="acl.json"
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

## Schema definition

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

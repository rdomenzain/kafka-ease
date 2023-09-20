from click.testing import CliRunner

from tests.test_base import TestBase
from src.main import cli


class TestCLI(TestBase):
    def test_topic_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_topic.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Topic name is required", result.output)

    def test_topic_default(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_topic_default.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "topic1: Topic num_partitions is required, "
            "using default value 1",
            result.output,
        )
        self.assertIn(
            "topic1: Topic replication_factor is required, "
            "using default value 1",
            result.output,
        )
        self.assertIn(
            "topic1: Topic cleanup_policy is required, "
            "using default value 'delete'",
            result.output,
        )
        self.assertIn(
            "topic1: Topic retention_days is required, "
            "using default value 7",
            result.output,
        )

    def test_acl_resource_type_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_resource_type.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ACL resource_type is required", result.output)

    def test_acl_resource_name_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_resource_name.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ACL resource_name is required", result.output)

    def test_acl_principal_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_principal.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ACL principal is required", result.output)

    def test_acl_host_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_host.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ACL host is required", result.output)

    def test_acl_operation_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_operation.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ACL operation is required", result.output)

    def test_acl_permission_type_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_permission_type.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ACL permission_type is required", result.output)

    def test_acl_pattern_type_error(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test_invalid_acl_pattern_type.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid pattern_type: INVALID", result.output)

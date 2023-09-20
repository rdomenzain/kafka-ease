from unittest import mock

from click.testing import CliRunner
from kafka.admin import KafkaAdminClient

from tests.test_base import TestBase
from src.main import cli


class TestCLI(TestBase):
    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)

    def test_command_apply(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["apply"])
        self.assertEqual(result.exit_code, 0)

    def test_command_apply_file_error(self):
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
                "tests/test.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "File tests/test.yml does not exists", result.output
        )

    def test_command_apply_file_json(self):
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
                "tests/files/test.json",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("JSON file detected", result.output)

    def test_command_apply_file_yaml(self):
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
                "tests/files/test.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("YAML file detected", result.output)

    def test_command_apply_file_not_supported(self):
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
                "tests/__init__.py",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "File extension not supported (only .json and .yaml/.yml",
            result.output,
        )

    def test_command_apply_file_validate(self):
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
                "tests/files/test.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("File tests/files/test.yml is valid.", result.output)

    def test_command_apply_invalid_cleanup_policy(self):
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
                "tests/files/test_invalid_01.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Topic cleanup_policy must be 'delete' or 'compact'", result.output
        )

    def test_command_apply_invalid_resource_type(self):
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
                "tests/files/test_invalid_02.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Invalid resource_type: INVALID, valid values are: UNKNOWN",
            result.output,
        )

    def test_command_apply_invalid_operation(self):
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
                "tests/files/test_invalid_03.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Invalid operation: INVALID, valid values are: ANY, ALL, READ",
            result.output,
        )

    def test_command_apply_invalid_permission_type(self):
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
                "tests/files/test_invalid_04.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Invalid permission_type: INVALID, valid values are: ANY, DENY",
            result.output,
        )

    def test_command_apply_invalid_security_protocol(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--security-protocol",
                "INVALID",
                "-f",
                "tests/files/test.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 2)
        self.assertIn(
            "Invalid value for '--security-protocol': 'INVALID' "
            "is not one of 'PLAINTEXT', 'SASL_PLAINTEXT'",
            result.output,
        )

    def test_command_apply_invalid_sasl_mechanism(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--sasl-mechanism",
                "INVALID",
                "-f",
                "tests/files/test.yml",
                "--only-validate",
            ],
        )
        self.assertEqual(result.exit_code, 2)
        self.assertIn(
            "Invalid value for '--sasl-mechanism': 'INVALID' is not one of "
            "'PLAIN', 'SCRAM-SHA-256', 'SCRAM-SHA-512'.",
            result.output,
        )

    @mock.patch.object(KafkaAdminClient, "__init__", return_value=None)
    @mock.patch.object(KafkaAdminClient, "list_topics")
    @mock.patch.object(KafkaAdminClient, "create_topics")
    @mock.patch.object(KafkaAdminClient, "create_acls")
    @mock.patch.object(KafkaAdminClient, "describe_acls")
    @mock.patch.object(KafkaAdminClient, "delete_acls")
    @mock.patch.object(KafkaAdminClient, "close")
    def test_command_apply_ok(
        self,
        mock_close,
        mock_delete_acls,
        mock_describe_acls,
        mock_create_acls,
        mock_create_topics,
        mock_list_topics,
        mock_kafka_admin,
    ):
        mock_close.return_value = None
        mock_delete_acls.return_value = True
        mock_describe_acls.return_value = ([], 1)
        mock_create_acls.return_value = True
        mock_create_topics.return_value = True
        mock_list_topics.return_value = []
        mock_kafka_admin.return_value = None
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--security-protocol",
                "PLAINTEXT",
                "--sasl-mechanism",
                "PLAIN",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test.yml",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Applying file...", result.output)
        self.assertIn("2 topics found.", result.output)
        self.assertIn("2 ACLs found.", result.output)
        self.assertIn("File synced successfully.", result.output)

    @mock.patch.object(KafkaAdminClient, "__init__", return_value=None)
    @mock.patch.object(KafkaAdminClient, "list_topics")
    @mock.patch.object(KafkaAdminClient, "alter_configs")
    @mock.patch.object(KafkaAdminClient, "create_acls")
    @mock.patch.object(KafkaAdminClient, "describe_acls")
    @mock.patch.object(KafkaAdminClient, "delete_acls")
    @mock.patch.object(KafkaAdminClient, "close")
    def test_command_apply_update_ok(
        self,
        mock_close,
        mock_delete_acls,
        mock_describe_acls,
        mock_create_acls,
        mock_alter_configs,
        mock_list_topics,
        mock_kafka_admin,
    ):
        mock_close.return_value = None
        mock_delete_acls.return_value = True
        mock_describe_acls.return_value = ([], 1)
        mock_create_acls.return_value = True
        mock_alter_configs.return_value = True
        mock_list_topics.return_value = [
            "topic1",
            "topic2",
        ]
        mock_kafka_admin.return_value = None
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--security-protocol",
                "PLAINTEXT",
                "--sasl-mechanism",
                "PLAIN",
                "--sasl-username",
                "admin",
                "--sasl-password",
                "SECRET",
                "-f",
                "tests/files/test.yml",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Applying file...", result.output)
        self.assertIn("2 topics found.", result.output)
        self.assertIn("2 ACLs found.", result.output)
        self.assertIn("File synced successfully.", result.output)

    def test_command_validate_brokers(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "-f",
                "tests/files/test.yml",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Kafka brokers not found.", result.output)

    def test_command_validate_username(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "-f",
                "tests/files/test.yml",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SASL username not found.", result.output)

    def test_command_validate_password(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "apply",
                "--kafka-brokers",
                "localhost:9092",
                "--sasl-username",
                "admin",
                "-f",
                "tests/files/test.yml",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SASL password not found.", result.output)

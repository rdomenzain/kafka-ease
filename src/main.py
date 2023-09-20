from click import ClickException, option, group, Choice
from dotenv import load_dotenv

from .command import Command

load_dotenv()


@group()
def cli():
    pass


@cli.command(name="apply")
@option(
    "--kafka-brokers",
    envvar="KAFKA_BROKERS",
    default=None,
    help="Kafka server to connect to use.",
)
@option(
    "--security-protocol",
    envvar="KAFKA_SECURITY_PROTOCOL",
    default="PLAINTEXT",
    type=Choice(["PLAINTEXT", "SASL_PLAINTEXT"]),
    help="Kafka Security protocol to use.",
)
@option(
    "--sasl-mechanism",
    envvar="KAFKA_SASL_MECHANISM",
    default="PLAIN",
    type=Choice(["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512"]),
    help="SASL mechanism to use.",
)
@option(
    "--sasl-username",
    envvar="KAFKA_SASL_USERNAME",
    default=None,
    help="SASL username to use.",
)
@option(
    "--sasl-password",
    envvar="KAFKA_SASL_PASSWORD",
    default="",
    help="SASL password to use.",
)
@option("--file", "-f", help="File path to validate")
@option(
    "--only-validate",
    default=False,
    is_flag=True,
    help="Only validate the file",
)
def apply(
    kafka_brokers: str,
    security_protocol: str,
    sasl_mechanism: str,
    sasl_username: str,
    sasl_password: str,
    file: str,
    only_validate: bool,
):
    """Apply configuration file with topics and ACL to Kafka.
    Args:
        kafka_brokers (str): Kafka server to connect to use.
        security_protocol (str): Kafka Security protocol to use.
        sasl_mechanism (str): SASL mechanism to use.
        sasl_username (str): SASL username to use.
        sasl_password (str): SASL password to use.
        file (str): File path to validate.
        only_validate (bool): Only validate the file.
    """
    try:
        cmd: Command = Command(
            kafka_brokers=kafka_brokers,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_username=sasl_username,
            sasl_password=sasl_password,
            file=file,
            only_validate=only_validate,
        )
        cmd.run()
    except Exception as e:
        raise ClickException(str(e))


if __name__ == "__main__":
    cli()

import os
import unittest


class TestBase(unittest.TestCase):
    def __init_subclass__(cls):
        if "KAFKA_BROKERS" in os.environ:
            del os.environ["KAFKA_BROKERS"]
        if "KAFKA_SECURITY_PROTOCOL" in os.environ:
            del os.environ["KAFKA_SECURITY_PROTOCOL"]
        if "KAFKA_SASL_MECHANISM" in os.environ:
            del os.environ["KAFKA_SASL_MECHANISM"]
        if "KAFKA_SASL_USERNAME" in os.environ:
            del os.environ["KAFKA_SASL_USERNAME"]
        if "KAFKA_SASL_PASSWORD" in os.environ:
            del os.environ["KAFKA_SASL_PASSWORD"]

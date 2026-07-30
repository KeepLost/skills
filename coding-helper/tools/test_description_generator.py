import json
import unittest

from description_generator import ErrorMessageGenerator


class ErrorMessageGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.generator = ErrorMessageGenerator()

    def test_generates_valid_json_for_supported_error_types(self):
        cases = {
            "NOT_FOUND": (
                {
                    "error_code": "CUSTOMER_NOT_FOUND",
                    "specific_message": "Customer CUST-42 was not found",
                    "how_to_resolve": "Check the customer ID",
                    "correct_format": "CUST-##",
                },
                {
                    "error": "CUSTOMER_NOT_FOUND",
                    "message": "Customer CUST-42 was not found",
                    "resolution": "Check the customer ID",
                    "example": "CUST-##",
                },
            ),
            "INVALID_INPUT": (
                {
                    "error_code": "INVALID_CUSTOMER_ID",
                    "field": "customer_id",
                    "received_value": "42",
                    "expected_format": "CUST-##",
                },
                {
                    "error": "INVALID_CUSTOMER_ID",
                    "message": "Invalid customer_id: 42",
                    "expected_format": "CUST-##",
                    "resolution": "Provide value matching CUST-##",
                },
            ),
            "RATE_LIMITED": (
                {
                    "error_code": "RATE_LIMITED",
                    "seconds": "30",
                },
                {
                    "error": "RATE_LIMITED",
                    "message": "Rate limit exceeded",
                    "retry_after": "30",
                    "resolution": "Wait 30 seconds before retrying",
                },
            ),
        }

        for error_type, (context, expected) in cases.items():
            with self.subTest(error_type=error_type):
                result = self.generator.generate(error_type, context)
                self.assertEqual(json.loads(result), expected)

    def test_unknown_error_type_falls_back_to_invalid_input(self):
        result = self.generator.generate(
            "UNKNOWN",
            {
                "error_code": "UNKNOWN",
                "field": "customer_id",
                "received_value": "bad-id",
                "expected_format": "CUST-##",
            },
        )

        self.assertEqual(
            json.loads(result),
            {
                "error": "UNKNOWN",
                "message": "Invalid customer_id: bad-id",
                "expected_format": "CUST-##",
                "resolution": "Provide value matching CUST-##",
            },
        )


if __name__ == "__main__":
    unittest.main()

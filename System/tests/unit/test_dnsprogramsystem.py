import unittest
from unittest.mock import patch
from dnsprogramsystem import generate_confusable_domains, check_domain_registration, analyze_domain_legitimacy

class TestDomainLegitimacyChecker(unittest.TestCase):

    def test_generate_confusable_domains(self):
        # Test for generating confusable domains
        self.assertIn("example.com", generate_confusable_domains("example.com"))  # basic inclusion

    @patch("dnsprogramsystem.dns.resolver.resolve")
    def test_check_domain_registration(self, mock_resolve):
        # Mocking DNS resolution
        mock_resolve.side_effect = [True, Exception('NXDOMAIN')]
        domains = ["registered.com", "unregistered.com"]
        result = check_domain_registration(domains)
        self.assertIn("registered.com", result)
        self.assertNotIn("unregistered.com", result)

    @patch("dnsprogramsystem.requests.get")
    def test_check_domain_with_virustotal(self, mock_get):
        # Mocking API response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "attributes": {
                    "last_analysis_stats": {"malicious": 1},
                    "last_analysis_results": {"test_scanner": {"category": "malicious", "result": "malware"}}
                }
            }
        }
        is_malicious, details = check_domain_with_virustotal("malicious.com")
        self.assertTrue(is_malicious)
        self.assertIsNotNone(details)

if __name__ == "__main__":
    unittest.main()

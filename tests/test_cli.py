import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "warehouse.cli", *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_quotes(self):
        for zone, standard, express in (
            ("local", "$8.00\n", "$15.00\n"),
            ("regional", "$11.00\n", "$18.00\n"),
        ):
            for args, expected in (
                ([], standard),
                (["--service", "standard"], standard),
                (["--service", "express"], express),
            ):
                with self.subTest(zone=zone, args=args):
                    result = self.run_cli("2", zone, *args)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, expected)

    def test_invalid_service(self):
        result = self.run_cli("2", "local", "--service", "overnight")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)
        self.assertEqual(result.stdout, "")

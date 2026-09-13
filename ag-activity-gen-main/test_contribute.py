import unittest
import contribute
from subprocess import check_output
from datetime import datetime


class TestContribute(unittest.TestCase):

    def test_arguments(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits, 10)
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_contributions_per_day(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_parse_specific_dates_default_format(self):
        """Test parsing dates with default YYYY-MM-DD format"""
        dates = contribute.parse_specific_dates("2026-09-13,2026-09-14")
        self.assertIsNotNone(dates)
        self.assertEqual(len(dates), 2)
        self.assertEqual(dates[0].date().isoformat(), "2026-09-13")
        self.assertEqual(dates[1].date().isoformat(), "2026-09-14")
        # Check time is set to 20:00
        self.assertEqual(dates[0].hour, 20)
        self.assertEqual(dates[0].minute, 0)

    def test_parse_specific_dates_custom_format(self):
        """Test parsing dates with custom format MM/DD/YYYY"""
        dates = contribute.parse_specific_dates("09/13/2026,09/14/2026", "%m/%d/%Y")
        self.assertIsNotNone(dates)
        self.assertEqual(len(dates), 2)
        self.assertEqual(dates[0].date().isoformat(), "2026-09-13")
        self.assertEqual(dates[1].date().isoformat(), "2026-09-14")

    def test_parse_specific_dates_single_date(self):
        """Test parsing a single date"""
        dates = contribute.parse_specific_dates("2026-09-13")
        self.assertIsNotNone(dates)
        self.assertEqual(len(dates), 1)
        self.assertEqual(dates[0].date().isoformat(), "2026-09-13")

    def test_parse_specific_dates_sorted(self):
        """Test that parsed dates are sorted"""
        # Provide unsorted dates
        dates = contribute.parse_specific_dates("2026-09-15,2026-09-13,2026-09-14")
        self.assertIsNotNone(dates)
        self.assertEqual(len(dates), 3)
        self.assertEqual(dates[0].date().isoformat(), "2026-09-13")
        self.assertEqual(dates[1].date().isoformat(), "2026-09-14")
        self.assertEqual(dates[2].date().isoformat(), "2026-09-15")

    def test_arguments_specific_dates(self):
        """Test argument parsing for --specific-dates"""
        args = contribute.arguments(['--specific-dates=2026-09-13,2026-09-14'])
        self.assertEqual(args.specific_dates, "2026-09-13,2026-09-14")
        self.assertEqual(args.date_format, "%Y-%m-%d")

    def test_arguments_date_format(self):
        """Test argument parsing for --date-format"""
        args = contribute.arguments(['--specific-dates=09/13/2026', '--date-format=%m/%d/%Y'])
        self.assertEqual(args.specific_dates, "09/13/2026")
        self.assertEqual(args.date_format, "%m/%d/%Y")

    def test_arguments_conventional_commits(self):
        """Test argument parsing for --conventional-commits"""
        args = contribute.arguments(['--conventional-commits'])
        self.assertTrue(args.conventional_commits)
        
        args_default = contribute.arguments([])
        self.assertFalse(args_default.conventional_commits)

    def test_message_format_legacy(self):
        """Test message format in legacy mode"""
        contribute.CONVENTIONAL_COMMITS = False
        test_date = datetime(2026, 9, 13, 14, 30)
        msg = contribute.message(test_date)
        self.assertIn("Contribution:", msg)
        self.assertIn("2026-09-13", msg)
        self.assertIn("14:30", msg)

    def test_message_format_conventional(self):
        """Test message format in conventional commits mode"""
        contribute.CONVENTIONAL_COMMITS = True
        test_date = datetime(2026, 9, 13, 14, 30)
        msg = contribute.message(test_date)
        self.assertIn("feat:", msg)
        self.assertIn("contribution on", msg)
        self.assertIn("2026-09-13", msg)
        self.assertIn("14:30", msg)
        # Reset to default
        contribute.CONVENTIONAL_COMMITS = False

    def test_commits(self):
        contribute.NUM = 11   # limiting the number only for unittesting
        contribute.main(['-nw',
                         '--user_name=sampleusername',
                         '--user_email=your-username@users.noreply.github.com',
                         '-mc=12',
                         '-fr=82',
                         '-db=10',
                         '-da=15'])
        self.assertTrue(1 <= int(check_output(
            ['git',
             'rev-list',
             '--count',
             'HEAD']
        ).decode('utf-8')) <= 20*(10 + 15))

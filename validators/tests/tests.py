from datetime import date
import unittest
from unittest.mock import patch

from marshmallow import ValidationError

from validators.validators import validator_date_limit_today


def fake_today():
    return date(year=2020, month=1, day=1)


class LogicTestCase(unittest.TestCase):
    def setUp(self):
        # Defining variables
        self.previous_date = date(year=2019, month=12, day=1)
        self.later_date = date(year=2020, month=1, day=2)
        self.positive_number = 5
        self.negative_number = -5

    '''
    '''

    @patch("validators.validators.date")
    def test_validator_date_limit_today(self, mock_today):
        # Set mock
        mock_today.today.return_value = fake_today()

        self.assertEqual(self.previous_date,
                         validator_date_limit_today(
                             self.previous_date))

        with self.assertRaises(ValidationError):
            validator_date_limit_today(self.later_date)


if __name__ == '__main__':
    unittest.main()

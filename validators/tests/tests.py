from datetime import date
import unittest
from unittest.mock import patch

from marshmallow import ValidationError

from validators.validators import (validator_date_limit_today,
                                   validator_no_negative, RentValidation)


def fake_today():
    return date(year=2020, month=1, day=1)


class ValidationsTestCase(unittest.TestCase):
    def setUp(self):
        # Defining variables
        self.previous_date = date(year=2019, month=12, day=1)
        self.later_date = date(year=2020, month=1, day=2)
        self.positive_number = 5
        self.negative_number = -5

    @patch("validators.validators.date")
    def test_validator_date_limit_today(self, mock_today):
        # Set mock
        mock_today.today.return_value = fake_today()

        self.assertEqual(self.previous_date,
                         validator_date_limit_today(
                             self.previous_date))

        with self.assertRaises(ValidationError):
            validator_date_limit_today(self.later_date)

    def test_validator_no_negative(self):
        self.assertEqual(self.positive_number,
                         validator_no_negative(self.positive_number))

        with self.assertRaises(ValidationError):
            validator_no_negative(self.negative_number)

    def test_validate_date_gt_max_limit(self):
        with self.assertRaises(ValidationError):
            date1 = date(year=2022, month=1, day=17)
            date2 = date(year=2022, month=1, day=1)
            RentValidation.validate_date_gt_max_limit(date1, date2, "test")

    def test_validate_date1_gr_or_eq_date2(self):
        with self.assertRaises(ValidationError):
            date1 = date(year=2022, month=1, day=1)
            date2 = date(year=2022, month=1, day=1)
            RentValidation.validate_date1_gr_or_eq_date2(date1, date2,
                                                         "test")

        with self.assertRaises(ValidationError):
            date1 = date(year=2022, month=1, day=1)
            date2 = date(year=2022, month=1, day=2)
            RentValidation.validate_date1_gr_or_eq_date2(date1, date2,
                                                         "test")

    def test_validate_date1_eq_or_low_date2(self):
        with self.assertRaises(ValidationError):
            date1 = date(year=2022, month=1, day=1)
            date2 = date(year=2022, month=1, day=1)
            RentValidation.validate_date1_eq_or_low_date2(date1, date2,
                                                          "test")

            date1 = date(year=2022, month=1, day=1)
            date2 = date(year=2022, month=1, day=2)
            RentValidation.validate_date1_eq_or_low_date2(date1, date2,
                                                          "test")


if __name__ == '__main__':
    unittest.main()

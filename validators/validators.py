import re
from marshmallow import ValidationError
from datetime import date

# New Validators
from bussiness_logic.bussiness_logic import RentBusinessLogic


def validate_email(email):
    if not email:
        raise ValidationError('No email provided')
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError('Provided email is not an email address')


def validate_phone(email):
    if not email:
        raise ValidationError('No email provided')
    if not re.match("\d{3}-\d{4}-\d{4}$", email):
        raise ValidationError('Provided email is not an email address')


def validate_film_type(film_type):
    if film_type not in ('movie', 'serie'):
        raise ValidationError('film_type should be movie or serie')


# Film Validators

def validator_date_limit_today(input_date: date) -> date:
    """
    Validate that the input date is not in the future

    Args:
        input_date (date): Input date

    Raises:
        ValidationError: The inserted date has not happened yet

    Return:
        input_date (date): Input date
    """
    if input_date > date.today():
        raise ValidationError("The inserted date has not happened yet")

    return input_date


def validator_date_limit_future(input_date: date) -> date:
    """
    Validate that the input date is  in the future

    Args:
        input_date (date): Input date

    Raises:
        ValidationError: The inserted date has not happened yet

    Return:
        input_date (date): Input date
    """
    if input_date < date.today():
        raise ValidationError("The inserted date shouldn't be in the past")

    return input_date


def validator_no_negative(num: int) -> int:
    """
    Validate that the number is not negative

    Args:
        num (int): Input number

    Raises:
        ValidationError: The inserted number has to be '0' or positive

    Return:
        num (int): Input number
    """
    if num < 0:
        raise ValidationError("The inserted number has to be '0' or positive")

    return num


# Rent Validators

amount_day_max_limit = 15


class RentValidation:
    """
    The class contains all the validations of the rent app
    """

    # Methods about validate date
    @classmethod
    def validate_date_gt_max_limit(cls, date1: date, date2: date, field: str):
        """
        Validate that the difference between both dates is not greater than max
         limit.

        Args:
            date1 (date): Input date1
            date2 (date): Input date2
            field (str): Indicate the field to report the ValidationError
        Raises:
            ValidationError: This return date has to be before the max limit
        """
        if RentBusinessLogic.get_date_diff_in_days(date1, date2) > \
                amount_day_max_limit:
            raise ValidationError(
                {field: (f'This return date has to be before'
                         f' {amount_day_max_limit} days from the start date')
                 })

    @staticmethod
    def validate_date1_gr_or_eq_date2(date1: date, date2: date, field: str):
        """
        Validate that date2 is not greater or equal than date2

        Args:
            date1 (date): Input date1
            date2 (date): Input date2
            field (str): Indicate the field to report the ValidationError
        Raises:
            ValidationError: date2 has to be after the date1
        """
        if date1 is not None:
            if date2 >= date1:
                raise ValidationError(
                    {field: ('This date has to be'
                             ' after the start date')
                     })

    @staticmethod
    def validate_date1_eq_or_low_date2(date1: date, date2: date, field: str):
        """
        Validate that date1 is not lower or equal than date2

        Args:
            date1 (date): Input date1
            date2 (date): Input date2
            field (str): Indicate the field to report the ValidationError

        Raises:
            ValidationError: date1 has to be after the date2
        """
        if date1 <= date2:
            raise ValidationError(
                {field: ('This date has to be'
                         ' after the start date')
                 })

    @staticmethod
    def validate_amount_availability(amount: int, film: 'Film'):
        """
        Validate that amount that the client is requesting is available

        Args:
            amount (date): Input date1
            film (date): Input date2

        Raises:
            ValidationError: The amount of film(s) that you are adding exceed
             the availability
        """
        film.availability -= amount

        if film.availability < 0:
            raise ValidationError(
                {'amount': ("The amount of film(s) that you are adding"
                            " exceed the availability"
                            f" ({film.availability})")})
        else:
            film.save()

    @classmethod
    def validate_amount_update(cls, current_amount: int, film: 'Film',
                               pre_save_rent):
        """
        Validate that the amount update process is it being executed correctly

        Args:
            current_amount (int): Amount of film to rent
            film (Film): Film to rent
            pre_save_rent (Rent): Pre save rent

        Raises:
            ValidationError: The film can't be change
        """

        # Film hasn't been change
        if pre_save_rent.film.id == film.id:
            cls.validate_amount_availability(
                (current_amount - pre_save_rent.amount), film)

        # The film have change
        else:
            raise ValidationError({'film': ("Once the film is saved"
                                            " it cannot be modified."
                                            " For this you have to create"
                                            " a new order.")})

    # Method about validate state
    @staticmethod
    def validate_state_close(state: str, actual_return_date: date):
        """
        Validate if is possible to close the rent base on state and actual
        return date

        Args:
            state (str): State of the rent
            actual_return_date (date):  Actual return date

        Raises:
            ValidationError: To change the state to close actual return date
            has to be different of None
        """
        if state == 'close' and actual_return_date is None:
            raise ValidationError({'state': ('To change the state to close'
                                             ' you have to first enter an'
                                             ' actual return date.')})

    # Methods for permission
    @staticmethod
    def validate_update_permission(state_presave: str):
        """
        If a rent is close put films available to rent again

        Args:
            state_presave (str): State of the rent before save

        Raises:
            ValidationError: You don't have permission to modify an already
             close rent
        """
        if state_presave == 'close':
            raise ValidationError("You don't have permission to modify"
                                  " an already close rent")

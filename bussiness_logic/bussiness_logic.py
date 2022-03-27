from marshmallow import ValidationError
from datetime import date

from utilities.logger import Logger

amount_day_max_limit = 15


class FilmBusinessLogic:
    """
    The class contains all the business logic of the film app
    """

    @staticmethod
    def validate_stock_greater_availability(stock: int, availability: int):
        """
        Validate that the stock is greater than availability

        Args:
            stock (int): stock of the film
            availability (int): availability of the film

        Raises:
            ValidationError: The availability shouldn't be higher than stock
        """
        if availability > stock:
            raise ValidationError({'availability': (
                "The availability shouldn't be higher than stock")})

    @staticmethod
    def validate_film_type_equal_prequel_film_type(film_type: str,
                                                   prequel_film_type: str):
        """
        Validate that type of the film and film prequel are equal

        Args:
            film_type (str): stock of the film
            prequel_film_type (str): availability of the film

        Raises:
            ValidationError: The film prequel should be the same type as the
             current film type
        """
        if prequel_film_type is not None:
            if film_type != prequel_film_type:
                raise ValidationError(
                    {'film_prequel': ('The film prequel should '
                                      'be the same type as '
                                      'the current film type. '
                                      '(Example both movie '
                                      'type)')})


class PersonBusinessLogic:
    """
    The class contains all the business logic of the person app
    """

    @staticmethod
    def get_age_by_birthday(birthday: date) -> date or str:
        """
        Validate that the stock is greater than availability

        Args:
            birthday (date): the birthday of the person

        Return:
            age (int): the current age of the person
            message (str): N.A, abbreviation for not applicable or not
            available
        """
        if birthday:
            return int((date.today() - birthday).days / 365.25)
        else:
            return "N.A"


class RentBusinessLogic:
    """
    The class contains all the business logic of the rent app
    """

    # Methods about obtain cost
    # I need to test this method, because is not working as expected
    @classmethod
    def get_rent_cost(cls, amount_film: int, star_date: date,
                      return_date: date, actual_return_date: date,
                      film_price_by_day: float):
        """
        Get the cost of renting the film

        Args:
            amount_film (int): Amount of film to rent
            star_date (date): Star date of the rent
            return_date (date): Return date of the rent
            actual_return_date (date): Actual return date of the rent
            film_price_by_day (float): The price by day of renting the film
        Return:
            cost (float): the cost of renting the film
            message (str): N.A, abbreviation for not applicable or not
            available
        """
        if actual_return_date is None:
            amount_days = cls.get_date_diff_in_days(return_date, star_date)
            cost = cls.get_theoretical_cost(amount_film, amount_days,
                                            film_price_by_day)

        else:
            cost = cls.get_actual_cost(amount_film, star_date, return_date,
                                       actual_return_date, film_price_by_day)

        if cost > 0:
            return cost

        Logger.debug(f"amount_film: {amount_film}")
        Logger.debug(f"star_date: {star_date}")
        Logger.debug(f"return_date: {return_date}")
        Logger.debug(f"actual_return_date: {actual_return_date}")
        Logger.debug(f"film_price_by_day: {film_price_by_day}")
        return 'N.A'

    @staticmethod
    def get_date_diff_in_days(date1: date, date2: date) -> int:
        """
        Get the difference in days between both dates

        Args:
            date1 (date): Input date1
            date2 (date): Input date1

        Return:
            days (int): amount of days of difference between the dates
        """
        date_difference = date1 - date2
        return date_difference.days

    @staticmethod
    def get_theoretical_cost(amount_film: int, amount_days: int,
                             film_price_by_day: float) -> float:
        """
        Get the theoretical cost without considering extra penalty costs

        Args:
            amount_film (int): Amount of films to rent
            amount_days (int): Theoretical amount of days to rent
            film_price_by_day (float): The price by day of renting the film

        Return:
            cost (float): the theoretical cost of renting the film
        """
        Logger.debug(f"amount_film: {amount_film}")
        Logger.debug(f"amount_days: {amount_days}")
        Logger.debug(f"film_price_by_day: {film_price_by_day}")
        cost = amount_film * amount_days * film_price_by_day
        Logger.debug(f"get_theoretical_cost: {cost}")
        return cost

    @staticmethod
    def get_extra_cost(amount_film: int, extra_days: int,
                       film_price_by_day: float) -> float:
        """
        Get the extra cost that means penalty costs for extra days

        Args:
            amount_film (int): Amount of films to rent
            extra_days (int):  Amount of extra days to rent
            film_price_by_day (float): The price by day of renting the film

        Return:
            cost (float): the extra cost of renting the film
        """
        Logger.debug(f"amount_film: {amount_film}")
        Logger.debug(f"film_price_by_day: {film_price_by_day}")
        Logger.debug(f"extra_days: {extra_days}")
        cost = extra_days * (amount_film * film_price_by_day + extra_days + 1)
        Logger.debug(f"get_extra_cost: {cost}")
        return cost

    @classmethod
    def get_actual_cost(cls, amount_film: int, star_date: date,
                        return_date: date, actual_return_date: date,
                        film_price_by_day: int) -> float:
        amount_days_normal_cost = cls.get_date_diff_in_days(return_date,
                                                            star_date)
        """
        Get the actual cost considering extra penalty costs

        Args:
            amount_film (int): Amount of film to rent
            star_date (date): Star date of the rent
            return_date (date): Return date of the rent
            actual_return_date (date): Actual return date of the rent
            film_price_by_day (float): The price by day of renting the film

        Return:
            cost (float): the actual cost of renting the film
        """

        Logger.debug(f"amount_days_normal_cost: {amount_days_normal_cost}")

        amount_days_actual_cost = cls.get_date_diff_in_days(actual_return_date,
                                                            star_date)

        Logger.debug(f"amount_days_actual_cost: {amount_days_actual_cost}")

        # Deliver before or on return_date
        if actual_return_date <= return_date:
            return cls.get_theoretical_cost(amount_film,
                                            amount_days_actual_cost,
                                            film_price_by_day)

        extra_days = amount_days_actual_cost - amount_days_normal_cost
        theorical_cost = cls.get_theoretical_cost(amount_film,
                                                  amount_days_normal_cost,
                                                  film_price_by_day)

        extra_cost = cls.get_extra_cost(amount_film, extra_days,
                                        film_price_by_day)

        actual_cost = theorical_cost + extra_cost

        Logger.debug(f"get_actual_cost: {actual_cost}")
        return actual_cost

    # Method about state
    @staticmethod
    def state_close_return_films(state: str, state_presave: str,
                                 amount: int, film: 'Film'):
        """
        If a rent is close put films available to rent again

        Args:
            state (str): State of the rent
            state_presave (str): State of the rent before save
            amount (int):  Amount of film to rent
            film (Film): film to rent
        """
        if state == 'close' and state_presave == 'open':
            film.availability += amount
            Logger.debug(f"film.availability:{film.availability}")
            Logger.debug(f"film.stock:{film.stock}")
            film.save()

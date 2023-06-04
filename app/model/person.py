from abc import ABC, abstractmethod


class Person(ABC):
    """
    Abstract helper class for inheritance
    and method implementation enforcement
    """

    def __init__(self, **kwargs) -> None:
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.gender = kwargs.get("gender")
        self.family_name = kwargs.get("family_name")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.place_of_birth = kwargs.get("place_of_birth")
        self.date_of_death = kwargs.get("date_of_death")
        self.place_of_death = kwargs.get("place_of_death")
        self.phone = kwargs.get("phone")
        self.email = kwargs.get("email")

    @abstractmethod
    def age(self) -> int:
        """
        Returns person age based on current date or years lived if deceased
        """
        raise NotImplementedError

    @abstractmethod
    def info(self) -> str:
        """ Prints all availible info about this person """
        raise NotImplementedError

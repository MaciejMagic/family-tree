from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Person(ABC):
    """
    Abstract helper class for inheritance
    and method implementation enforcement.
    """

    def __init__(self, **kwargs) -> None:
        self.first_name: str = kwargs.get("first_name")
        self.last_name: str = kwargs.get("last_name")
        self.gender: str = kwargs.get("gender")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.place_of_birth: str = kwargs.get("place_of_birth")
        self.date_of_death = kwargs.get("date_of_death")
        self.place_of_death: str = kwargs.get("place_of_death")

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


@dataclass
class PersonData:
    """
    Helper class for Relatives personal data
    """
    family_name: str = None
    phone: str = None
    email: str = None
    events: list[str] = field(default_factory=list)
    desc: list[str] = field(default_factory=list)


@dataclass
class FamilyData:
    """
    Helper class for Relatives family data
    """
    # Values from other Persons self.id column
    mother: int = None
    father: int = None
    spouse_current: int = None
    children: list[int] = field(default_factory=list)

    married: bool = False

    def __post_init__(self) -> None:
        if self.spouse_current is not None:
            self.married = True
        self.married = False

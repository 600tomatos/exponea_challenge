from abc import ABC, abstractmethod


class ValidatorInf(ABC):
    """Base class for validators"""

    @classmethod
    def check(cls, value):
        """Helper method that takes out the logic of creating a validator outside view.
           It is understood that validation begins with the perform_validate method.
        """

        return cls().perform_validate(value)

    @abstractmethod
    def perform_validate(self, *args, **kwargs):
        """Any additional logic that can break validation into smaller logical parts"""

        pass

    def validate(self, *args, **kwargs):
        """
        The main validation method.
        Pass value thorough all validators.
        """

        available_validators = [func for func in dir(self) if func.startswith('validate_')]
        for validator in available_validators:
            current_validator = getattr(self, validator)
            error = current_validator(*args, **kwargs)
            if error:
                return error

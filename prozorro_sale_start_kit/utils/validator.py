from prompt_toolkit.validation import Validator, ValidationError
import re


def name_type(name: str) -> str:
    """
    The validator for the name argument.
    """

    if not re.match(r"^[a-zA-Z0-9_-]*$", name):
        raise NameError(
            "The format of the project name is incorrect."
        )
    return name


def name_underscore_type(name: str) -> str:
    """
    The validator for the name argument.
    """

    if not re.match(r"^[a-zA-Z0-9_]*$", name):
        raise NameError(
            "The format of the project underscore name is incorrect."
        )
    return name


class ProjectNameValidator(Validator):

    def validate(self, name):
        try:
            name_type(name.text)
        except NameError:
            raise ValidationError(
                message='Please enter a valid project name. Name can only contain these a-zA-Z0-9_- characters',
                cursor_position=len(name.text))
        else:
            if name.text == 'MyExampleProject':
                raise ValidationError(
                    message='Please clean default project name and enter you',
                    cursor_position=len(name.text))

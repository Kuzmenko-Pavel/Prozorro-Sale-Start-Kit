from prompt_toolkit.validation import Validator, ValidationError
import re


ip_middle_octet = r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
ip_last_octet = r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"

regex_url = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    r"(?P<private_ip>"
    # IP address exclusion
    # private & local networks
    r"(?:(?:10|127)" + ip_middle_octet + r"{2}" + ip_last_octet + r")|"
    r"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + r")|"
    r"(?:172\.(?:1[6-9]|2\d|3[0-1])" + ip_middle_octet + ip_last_octet + r"))"
    r"|"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?P<public_ip>"
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"" + ip_middle_octet + r"{2}"
    r"" + ip_last_octet + r")"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    # query string
    r"(?:\?\S*)?"
    r"$",
    re.UNICODE | re.IGNORECASE
)

pattern_url = re.compile(regex_url)


def name_type(name: str) -> str:
    """
    The validator for the name argument.
    """

    if not re.match(r"^[a-zA-Z0-9_-]*$", name):
        raise NameError(
            "The format of the project name is incorrect."
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


class ProjectLinkValidator(Validator):

    def validate(self, link):
        if not pattern_url.match(link.text):
            raise ValidationError(
                message='Please enter a valid link to you GitLab Projects',
                cursor_position=len(link.text))

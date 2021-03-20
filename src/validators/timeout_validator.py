from interfaces.validator import ValidatorInf


class TimeoutValidator(ValidatorInf):

    def perform_validate(self, request):
        """Implement base perfom validate method"""

        # get timeout from request
        timeout = request.args.get('timeout')
        return self.validate(timeout)

    def validate_value(self, timeout):
        if timeout is None:
            return 'Timeout is required.'
        try:
            int(timeout)
        except Exception:
            return 'Timeout can be a string, but the string represent a valid number. Your value is not valid'

    def validate_type(self, timeout):
        if not isinstance(timeout, (int, float, str)):
            return 'Only integer or float are acceptable for timeout'

    def validate_range(self, timeout):
        if timeout is not None:
            try:
                timeout = int(timeout)
                if timeout < 1:
                    return 'Only positive values of integer or float are acceptable for timeout'
            except Exception:
                ...

from datetime import date
import re


class Validator(object):

    _fields = {
        "first_name": {'validators': []},
        "last_name": {'validators': []},
        "country_code": {'validators': ['_check_if_in_list']},
        "phone_number": {'validators': ['_is_valid_phone', '_is_num', '_is_available', '_length_checker']},
        "gender": {'validators': ['_check_if_in_list']},
        "birthdate": {'validators': ['_check_date']},
        "avatar": {'validators': ['_check_avatar']},
        "email": {'validators': []},
    }
    country_code_list = ['EG', 'KSA', 'UK', 'KW']
    gender_list = ['MALE', 'FEMALE']

    def __new__(cls, field_name, value=None, model=None, *args, **kwargs):
        _error_list = []

        if field_name == 'email':
            if value == '':
                return True, None
            else:
                s1, v1 = cls._is_email(value)
                if s1:
                    return cls._is_available(v1, 'email', model)
                else:
                    return s1, v1

        if value == '' or value is None:
            return False, {'error': 'blank'}

        for validator in cls._fields[field_name]['validators']:
            validator_func = getattr(Validator, validator)
            status, validated_value = validator_func(value, field_name, model)

            if status:
                pass
            else:
                _error_list.append(validated_value)

        if not _error_list:
            return [True, value]

        else:
            return False, _error_list

    @staticmethod
    def _is_email(value, *args):
        regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
        return [True, value] if re.fullmatch(regex, value) else [False, {"error": "invalid"}]

    @staticmethod
    def _is_num(value, *args):
        return [True, value] if value[1:].isnumeric() else [False, {'error': 'not_a_number'}]

    @staticmethod
    def _is_available(value, field, model):
        return [True, value] if list(model.objects.filter(**{field: value})) == [] else [False, {'error': 'taken'}]

    @staticmethod
    def _length_checker(value, *args):
        if len(value) >= 15:
            return [False, {'error': 'too_long', 'count': len(value)}]
        elif len(value) <= 10:
            return [False, {'error': 'too_short', 'count': len(value)}]
        else:
            return [True, value]

    @staticmethod
    def _check_if_in_list(value, field_name, *args):
        value = value.upper()
        return [True, value] if value in getattr(Validator, f'{field_name}_list') else [False, {"error": "inclusion"}]

    @staticmethod
    def _check_avatar(value, *args):
        allowed_extensions = ['jpg', 'jpeg', 'png']
        return [True, value] if value in allowed_extensions else [False, {"error": "invalid_content_type"}]

    @staticmethod
    def _check_date(value, *args):
        return [True, value] if (date.today() - date(*[int(v) for v in value.split('-')])).days >= 0\
            else [False, {"error": "in_the_future"}]

    @staticmethod
    def _is_valid_phone(value, *args):
        regx = r'\+\d{10,13}'
        return [True, value] if re.fullmatch(regx, value) else [False, {"error": "invalid"}]


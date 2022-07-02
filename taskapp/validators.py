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
    country_code_list = ['AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ',
                         'BH', 'BS', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW', 'BV', 'BR',
                         'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC',
                         'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO',
                         'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA',
                         'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT',
                         'HM', 'VA', 'HN', 'HK', 'HU', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IM', 'IT', 'JM', 'JP', 'JE',
                         'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT',
                         'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM',
                         'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE',
                         'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL',
                         'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM',
                         'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'SS', 'ES',
                         'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO',
                         'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VE',
                         'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW' 'AFG', 'ALA', 'ALB', 'DZA', 'ASM', 'AND', 'AGO',
                         'AIA', 'ATA', 'ATG', 'ARG', 'ARM', 'ABW', 'AUS', 'AUT', 'AZE', 'BHS', 'BHR', 'BGD', 'BRB',
                         'BLR', 'BEL', 'BLZ', 'BEN', 'BMU', 'BTN', 'BOL', 'BES', 'BIH', 'BWA', 'BVT', 'BRA', 'IOT',
                         'VGB', 'BRN', 'BGR', 'BFA', 'BDI', 'KHM', 'CMR', 'CAN', 'CPV', 'CYM', 'CAF', 'TCD', 'CHL',
                         'CHN', 'CXR', 'CCK', 'COL', 'COM', 'COK', 'CRI', 'HRV', 'CUB', 'CUW', 'CYP', 'CZE', 'COD',
                         'DNK', 'DJI', 'DMA', 'DOM', 'TLS', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'ETH', 'FLK',
                         'FRO', 'FJI', 'FIN', 'FRA', 'GUF', 'PYF', 'ATF', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA', 'GIB',
                         'GRC', 'GRL', 'GRD', 'GLP', 'GUM', 'GTM', 'GGY', 'GIN', 'GNB', 'GUY', 'HTI', 'HMD', 'HND',
                         'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ', 'IRL', 'IMN', 'ITA', 'CIV', 'JAM',
                         'JPN', 'JEY', 'JOR', 'KAZ', 'KEN', 'KIR', 'XXK', 'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LSO',
                         'LBR', 'LBY', 'LIE', 'LTU', 'LUX', 'MAC', 'MKD', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI', 'MLT',
                         'MHL', 'MTQ', 'MRT', 'MUS', 'MYT', 'MEX', 'FSM', 'MDA', 'MCO', 'MNG', 'MNE', 'MSR', 'MAR',
                         'MOZ', 'MMR', 'NAM', 'NRU', 'NPL', 'NLD', 'ANT', 'NCL', 'NZL', 'NIC', 'NER', 'NGA', 'NIU',
                         'NFK', 'PRK', 'MNP', 'NOR', 'OMN', 'PAK', 'PLW', 'PSE', 'PAN', 'PNG', 'PRY', 'PER', 'PHL',
                         'PCN', 'POL', 'PRT', 'PRI', 'QAT', 'COG', 'REU', 'ROU', 'RUS', 'RWA', 'BLM', 'SHN', 'KNA',
                         'LCA', 'MAF', 'SPM', 'VCT', 'WSM', 'SMR', 'STP', 'SAU', 'SEN', 'SRB', 'SCG', 'SYC', 'SLE',
                         'SGP', 'SXM', 'SVK', 'SVN', 'SLB', 'SOM', 'ZAF', 'SGS', 'KOR', 'SSD', 'ESP', 'LKA', 'SDN',
                         'SUR', 'SJM', 'SWZ', 'SWE', 'CHE', 'SYR', 'TWN', 'TJK', 'TZA', 'THA', 'TGO', 'TKL', 'TON',
                         'TTO', 'TUN', 'TUR', 'TKM', 'TCA', 'TUV', 'VIR', 'UGA', 'UKR', 'ARE', 'GBR', 'USA', 'UMI',
                         'URY', 'UZB', 'VUT', 'VAT', 'VEN', 'VNM', 'WLF', 'ESH', 'YEM', 'ZMB', 'ZWE'
                         ]

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

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from random import randint
from .models import User, Status
from .validators import Validator

# Create your tests here.

_user_template = {
    'first_name': "user_first_name",
    'last_name': "user_last_name",
    "phone_number": f"+0109{randint(1000, 2000)}8911",
    "country_code": "EG",
    "gender": "male",
    "birthdate": "2022-06-29",
    "password": 'abcd123'
}

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
image = SimpleUploadedFile('small.png', small_gif, content_type='image/png')
invalid_image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')


class ModelsTest(TestCase):

    @staticmethod
    def create_user():
        return User.objects.create(**_user_template)

    def test_user_model(self):
        user = self.create_user()
        self.assertEqual(user.username, user.phone_number)
        self.assertEqual(user.__str__(), f'{user.first_name} {user.last_name}')

    def test_status_model(self):
        user = self.create_user()
        status = Status.objects.create(user=user, status='active')
        self.assertEqual(status.__str__(), f'{status.user} => ({status.status})')


class APIViewsTest(APITestCase):

    @staticmethod
    def create_user():
        return User.objects.create(**{**_user_template, 'phone_number': '+01012345678'})

    @staticmethod
    def create_token():
        user = User.objects.create(**_user_template)
        return user, Token.objects.get_or_create(user=user)

    def test_user_successful_creation(self):
        response = self.client.post('/api/create/', data={**_user_template, 'avatar': image})
        self.assertEqual(response.status_code, 201)

    def test_user_field_creation(self):
        response = self.client.post('/api/create/', data={**_user_template, 'avatar': invalid_image})
        self.assertEqual(response.status_code, 400)

    def test_check_avatar_is_blank(self):
        response = self.client.post('/api/create/', data={'avatar': ''})
        self.assertEqual(response.status_code, 400)

    # def test_token_creation_success(self):
    #     user = self.create_user()
    #     user.is_active = True
    #     user.save()
    #     response = self.client.post('/api/login/',
    #                                 data={'phone_number': '+01012345678', 'password': 'abcd123'}
    #                                 )
    #     print(50 * '-')
    #     print(response)
    #     print(50 * '-')
    #     self.assertEqual(response.status_code, 200)

    def test_token_creation_failed_invalid_data(self):
        user = self.create_user()
        user.is_active = True
        user.save()
        response = self.client.post('/api/login/',
                                    data={'phone_number': '+123', 'password': 'abcd123'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_token_creation_failed_no_data(self):
        user = self.create_user()
        user.is_active = True
        user.save()
        response = self.client.post('/api/login/')
        self.assertEqual(response.status_code, 400)

    def test_status_creation_success(self):
        user, token = self.create_token()
        response = self.client.post('/api/status/', data={
            'token': token[0],
            'status': 'active',
            'phone_number': user.phone_number
        })
        self.assertEqual(response.status_code, 201)

    def test_status_creation_failed_in_token_validation(self):
        response = self.client.post('/api/status/', data={
            'token': 'no_token',
            'status': 'active',
            'phone_number': 'no_phone'
        })
        self.assertEqual(response.status_code, 401)

    def test_status_creation_failed_in_phone_validation(self):
        user, token = self.create_token()
        response = self.client.post('/api/status/', data={
            'token': token[0],
            'status': 'active',
            'phone_number': 'no_phone'
        })
        self.assertEqual(response.status_code, 401)

    def test_status_creation_failed_in_creation(self):
        user, token = self.create_token()
        response = self.client.post('/api/status/', data={
            'token': token[0],
            'status': '',
            'phone_number': user.phone_number
        })
        self.assertEqual(response.status_code, 400)


class ValidatorTest(TestCase):

    @staticmethod
    def create_user():
        return User.objects.create(**{**_user_template, 'email': 'check@not.av'})

    def test_too_long_phone(self):
        phone = '+000000000000000'
        _, value = Validator._length_checker(value=phone)
        self.assertEqual(value, {'error': 'too_long', 'count': len(phone)})

    def test_too_short_phone(self):
        phone = '+0000'
        _, value = Validator._length_checker(value=phone)
        self.assertEqual(value, {'error': 'too_short', 'count': len(phone)})

    def test_check_is_email(self):
        email = 'm@g.co'
        not_email = 'a123.com'
        _, value = Validator._is_email(value=email)
        self.assertEqual(value, email)
        _, value = Validator._is_email(value=not_email)
        self.assertEqual(value, {'error': 'invalid'})

    def test_is_blank_checker(self):
        _, value = Validator(field_name='first_name', value='', model=User)
        self.assertEqual(value, {'error': 'blank'})

    def test_blank_email(self):
        _, value = Validator(field_name='email', value='', model=User)
        self.assertEqual(value, None)

    def test_check_if_email_is_available(self):
        email = 'email@user.com'
        _, value = Validator(field_name='email', value=email, model=User)
        self.assertEqual(value, email)

    def test_check_if_email_is_not_available(self):
        _, value = Validator(field_name='email', value='test.not.email', model=User)
        self.assertEqual(value, {"error": "invalid"})


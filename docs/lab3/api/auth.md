# Auth API




### `/auth/users/` (Without authentication token)
> Request: `GET`

Response 401:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### `/auth/users/` (Registering a new user)
> Request: `POST`

Body:
```json
{
        "username": "User1",
        "password": "MyPassword1234",
        "email": "",
        "last_name": "",
        "first_name": "",
        "middle_name": "",
        "serial_number": "0000",
        "passport": "",
        "address": "",
        "education_level": "",
        "phone_number": "",
        "academic_degree": null,
        "date_of_birth": null,
        "library": null,
        "reading_room": null
}
```

Response 201:
```json
{
    "serial_number": "0000",
    "username": "User1",
    "id": 9
}
```

## `/auth/token/login` (Getting token)
> Request: `POST`


Body:
```json
{
    "username": "User1",
    "password": "MyPassword1234"
}
```

Response 200:
```json
{
    "auth_token": "732c303a48cb693fce9282f9716a72e671b9f755"
}
```


### `/auth/users/` (With authentication token)
> Request: `GET`
> Headers: `Authorization: Token 732c303a48cb693fce9282f9716a72e671b9f755`


Response 200:
```json
[
    {
        "id": 9,
        "username": "User1",
        "email": "",
        "last_name": "",
        "first_name": "",
        "middle_name": "",
        "serial_number": "0000",
        "passport": "",
        "address": "",
        "education_level": "",
        "phone_number": "",
        "academic_degree": null,
        "date_of_birth": null,
        "library": null,
        "reading_room": null,
        "readingroombookuser_set": []
    }
]
```

## `/auth/token/logout` (Invalidating token)
> Request: `POST`


Body:
```json
{
    "auth_token": "732c303a48cb693fce9282f9716a72e671b9f755"
}
```

Response 200:
```json

```
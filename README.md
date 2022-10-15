to run the app, type in root

```
poetry shell
poetry install
cd tag_a_bird_backend
flask run
```
## API routes
`/signup` Send a `POST` request to sign up a new user, usage:
```
{
    "id": "234",
    "username": "test",
    "email": "test@test.com",
    "password": "12345"
}
```

## Testing
for running tests, type 
```
python -m pytest
```
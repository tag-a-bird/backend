
to run the app, type in root

```
poetry shell
poetry install
cd tag_a_bird_backend
flask run
```
## API routes
`api/users` Send a `GET` request to check all users.

`api/signup` Send a `POST` request to sign up a new user, usage:
```
{
    "username": "test",
    "email": "test@test.com",
    "password": "12345"
}
```
`/api/annotation` protected route for annotation.

## Testing
for running tests, type 
```
python -m pytest
```
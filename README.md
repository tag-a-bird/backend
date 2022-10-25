to run the app, type in root

```
poetry shell
poetry install
cd tag_a_bird_backend
flask run
```
## API routes
`/api/signup` Send a `POST` request to sign up a new user, usage:
```
{
    "username": "test",
    "email": "test@test.com",
    "password": "12345"
}
```
`/api/signin` Send a `POST` request to sign in with the credentials of an existing user. 

`/api/signout` Send a `GET` request. logout_user() of LoginManager will handle signing out. 

### Test routes
`/api/annotation` protected Resource for testing, `GET` enabled.

## Testing
for running tests, type 
```
pytest -v -p no:warnings
```

Note: Blueprint registering return several warnings. "...Make sure all imports, decorators, functions, etc. needed to set up the blueprint are done before registering it. This warning will become an exception in Flask 2.3."
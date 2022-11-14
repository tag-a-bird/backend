to run the app, type in root

```
poetry shell
poetry install
cd tag_a_bird_backend
flask run
```
## API routes
`/api/register` Send a `POST` request to register a new user, usage:
```
{
    "username": "test",
    "email": "test@test.com",
    "password": "12345"
}
```
`/api/login` Send a `POST` request to log in with the credentials of an existing user. 

`/api/logout` Send a `GET` request. logout_user() of LoginManager will handle logging out. 


## Testing
for running tests, type 
```
pytest -v 
```
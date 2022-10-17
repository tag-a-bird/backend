
to run the app, type in root

```
poetry shell
poetry install
cd tag_a_bird_backend
flask run
```
## API routes
`api/signup` Send a `POST` request to sign up a new user, usage:
```
{
    "username": "test",
    "email": "test@test.com",
    "password": "12345"
}
```
`api/signup` Send a `POST` request to sign in with the credentials of an existing user. At this step a JWT gets generated. 

`api/users` Send a `GET` request to check all users. Protected route, only with JWT can be accessed. 

`'/api/signout'` Send a `DELETE` request to revoke current JWT. 

### Test routes
`'/api/protected'` Send a `GET` request - only for testing. 

`/api/annotation` open Resource for annotation, `GET` enabled.

`/api/annotation` protected Resource for testing, `GET` enabled.

## Testing
for running tests, type 
```
python -m pytest
```
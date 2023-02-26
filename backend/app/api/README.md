# API inner structure documentation

You can find API endpoints description [here](https://kennelteam.github.io/sol-db-in/)

We use FlaskRESTFul for requests processing. So each endpoint is represented 
by a class inherited from `flask_restful.Resourse`. 
In [`backend/app/routes.py`](../../../backend/app/routes.py)
we bind the classes with their endpoints. To bind your class, you should
add `route` field to your class and add your class to the resources list in 
[`backend/app/routes.py`](../../../backend/app/routes.py)

## Common ideas
We use `GET` requests for getting info and `POST` requests for 
creating and updating objects.\
There are some helpful stuff in
[auxiliary.py](auxiliary.py):
- `HTTPErrorCode` enum. If some error occurred, the response should be like:\
`{"error": "SOME_HTTP_ERROR_CODE_ELEMENT"}`
- `get_class_item_by_id_request(Class)` - a very common type of `GET` requests
looks like this: get a database item by its ID. This function does right this 
work with a given class (`Class` should be a database Model class)
- `create_standard_reqparser()` - a very common template of request is this:\
`{"id": id, "name": ...(TranslatedText), "deleted": false, ...(more arguments)}`
This function adds to the parser those 3 arguments and returns the parser
- `standard_text_object_update(Class, arguments)` - gets and item of `Class` 
class and updates it with standard values from request arguments 
(standard values are `name` and `deleted`)
- `get_request(min_access_level) and post_request(min_access_level)` 
are decorators for our `GET` and `POST/PUT` requests respectively. 
It checks access rights of the user for the API endpoint and does some 
preparations for work with DB (in case of `POST/PUT` method). 
You can leave the argument empty - then it'll have a 
default access level for this type of request
- `get_failure(error, status)` and `post_failure(error, status)` are functions
for correct error return. `error` is `HTTPErrorCode` element and `status` is
`REST` response status. This function correctly finishes the request processing
and returns the correct response object
- `check_json_format(source, json_format)` helps with checking that request
arguments have correct formats. Some database classes provide `json_format`
method. So you can check if the given `JSON` object satisfies the format of the
database object like this: `check_json_format(given_json, DBModelClass.json_format())`\
The function returns an `HTTPErrorCode` of the error 
(`HTTPErrorCode.SUCCESS` if everything is OK)

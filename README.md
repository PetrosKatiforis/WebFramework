# Simple Python Web Framework

This repository consists of a simple web framework written in python. 
The code follows a basic Request-Response pattern.

Some of the framework's features:
  - Template support using Jinja2
  - Static files with whitenoise
  - Url parameters `` /users/{username} `` using the parse library.
  - Class-based and function handlers with the ``app.route()`` decorator
  - Respond to different methods using the `` request.method `` attribute or by naming your class methods after the request's name


## Sample Usage

```python
from WebFramework import WebApplication
app = WebApplication()

@app.route("/")
class HomePage:
    def get(self, request, response):
        context = { "heading": "Hello World!", "status": response.status }
        response.body = app.template("index.html", context)
    	
    def post(self, request, response):
        response.content_type = "application/json"
        response.body = {
            "message": "This is a post request!",
            "is_template": False
        }

@app.route("/users/{username}")
def user_page(request, response, username):
    response.body = f"Hello, <h1>{username}</h1>"
```

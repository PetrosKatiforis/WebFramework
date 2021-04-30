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

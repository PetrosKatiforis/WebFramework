from .route import Route
from .response_request import Response, Request
from .utils import create_jinja_environment
from whitenoise import WhiteNoise
import inspect

class WebApplication:
    def __init__(self, templates_path="templates", static_path="static"):
        self.routes_map = {}
        self.templates = create_jinja_environment(templates_path)
        self.whitenoise = WhiteNoise(self.wsgi_main, root=static_path)

    def template(self, template_name, context={}):
        """
        Renders a Jinja2 template

        :param template_name: The filename of the tempalte to be rendered
        :param context: The Jinja context that will be passed on the template 
        :returns: The loaded template
        """

        return self.templates.get_template(template_name).render(**context)

    def wsgi_main(self, environ, start_response):
        """
        Callable following the PEP333 WSGI standards

        :param environ: A dictionary containing request and server information
        :param start_response: A callable which accepts the status and the headers of the request 
        """

        request = Request(environ)

        response = self.handle_request(request)
        
        return response(environ, start_response)
    
    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)
        
    def route(self, path):
        """
        A decorator that wraps HTTP routes
        
        :param path: The url path that will trigger the handler
        """

        def wrapper(handler):
            self.routes_map[path] = Route(path, handler)
            return handler
            
        return wrapper

    def default_response(self, response):
        response.body = "<h1>Not Found.</h1>"
        response.status_code = "404"

    def find_handler(self, target_path):
        """
        Searches and finds the apprpriate handler with the help of the parse library

        :param target_path: The url path assosiated with the handler
        :returns: The handler function with the parsed url parameters
        """

        for path, route in self.routes_map.items():
            parse_result, is_match = route.check_match(target_path)
            
            if is_match:
                return route.handler, parse_result.named

        return None, None

    def handle_request(self, request):
        """
        Handles an HTTP request

        :returns: Calls the handler and returns the response according to the request's path. 
        If that's not found, it will return a default 404 response.
        """

        response = Response()
        handler, kwargs = self.find_handler(request.path)
        
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower())

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

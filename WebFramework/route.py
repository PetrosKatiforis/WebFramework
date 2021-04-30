from parse import parse

class Route:
    def __init__(self, pattern, handler):
        self.pattern = pattern
        self.handler = handler
        
    def check_match(self, pattern):
        """
        Check if the route's pattern matched the request
        
        :param pattern: String, request's url
        :returns: A tuple of the parsed result followed by an "is_match" boolean 
        """
        
        parse_result = parse(self.pattern, pattern)
        is_match = parse_result is not None
        
        return parse_result, is_match

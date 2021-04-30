from jinja2 import Environment, FileSystemLoader
import os

def create_jinja_environment(templates_path):
    """
    Initializes and returns a Jinja2 environment

    :param templates_path: Path to the templates' directory
    """

    JinjaLoader = FileSystemLoader(os.path.abspath(templates_path))
    
    return Environment(loader=JinjaLoader)
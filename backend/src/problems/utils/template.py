from jinja2 import Environment, FileSystemLoader


def render_template(template_name, data):
    """
    Render a Jinja2 template with the given data.
    
    Args:
        template_name (str): Name of the template file (e.g., 'problem_templates/arithmetic_intensity.j2')
        data (dict): Data to pass to the template
    
    Returns:
        str: Rendered template content
    """
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    return template.render(data)

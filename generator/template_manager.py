from jinja2 import Environment, FileSystemLoader
from .freemarker_generator import generate_template
from pathlib import Path

def render_template(template_dir: Path, file_type: str, spec: dict):
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    ftl_file = file_type + ".ftl"
    ftl_path = template_dir / ftl_file

    generate_template(str(ftl_path), file_type, spec)

    template = env.get_template(ftl_file)
    return template.render(**spec)
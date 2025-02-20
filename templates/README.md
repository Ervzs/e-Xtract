### `templates/` (HTML Templates)
- Stores all HTML files used for rendering views.
- Flask uses Jinja2 templating, allowing dynamic content generation.
  - Flask relies on Jinja2 on default
  - Jinja2 is responsible for template inheritance, control structures, and variable handling
- Keeping templates separate from python files ensures a clear separation of concerns.

### `templates/base.html` (Parent Template)
-  serves as a layout template that other pages or child template inherits.
- Uses `{% block %}` for Dynamic Content: Child templates override only specific sections while keeping the rest intact.
- **Improves Maintainability**: Changes to global UI elements (like navigation bars) affect all pages automatically.
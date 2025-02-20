### `blueprints/__init__.py` (Main App Initialization)
- This `__init__.py` creates the Flask app.
- Registers the blueprints (`extract_bp`, `routing_bp`, `views_bp`), allowing different parts of the app to work independently.
- `__init__.py`, making everything inside blueprints/ accessible.


### `blueprints/views.py` (Handles Page Routes)

### When app.py calls create_app(), it:
- Creates a Flask app instance.
- Sets static_folder and template_folder.
- Registers the blueprints (`views_bp`, `extract_bp`, `routing.py`).
- Returns the configured app.

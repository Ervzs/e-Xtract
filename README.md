# Project Structure Overview

The organization is divided into categories based on functionality, as described below.

---

## Structure

- [BLUEPRINTS](#blueprints)
  - MODELS
    - chatbot
    - image-proc
    - extract.py
  - ROUTING
    - routing.py
  - VIEWS
    - views.py
- [STATIC](#static)
  - images folder
  - js src
  - css src
- [TEMPLATES](#templates)
  - html srcs

---

## Explanation

### BLUEPRINTS

Under the `blueprints` folder, the functionality is organized into the following categories:

- **MODELS** contains logic for handling models:
  - **chatbot**: Contains logic for chatbot functionality.
  - **image-proc**: Handles image processing logic.
  - **extract.py**: Responsible for rendering `extract.html`.

   ***Note**: The following can be modified as needed depending on further research and decisions*

- **ROUTING** is responsible for backend routing logic:
  - **routing.py**: Contains backend logic for routing, including the **disposal routing** algorithm (Dijkstra's) and rendering of the `disposal-sites.html` page.

- **VIEWS** contains the rendering logic for HTML files:
  - **views.py**: Primarily responsible for rendering HTML pages with minimal to no backend logic.

---

### STATIC

The `static` folder stores all static files that are served directly to the user. These files include images, CSS, and JavaScript assets.

- **images folder**: Stores images like logos, icons, and other visuals.
- **css src**: Contains the CSS files for styling the web pages.
- **js src**: Contains JavaScript files for handling frontend logic.

> **Note**: You may create separate subfolders inside `static` for better organization (e.g., `css`, `js`).

---

### TEMPLATES

The `templates` folder contains all HTML files that are rendered by Flask. Flask will look for the HTML templates in this folder.

---

### Linking Static Files in Templates

To link static files (CSS, JS, images) in your templates, use the following syntax:

#### CSS
```html
<link rel="stylesheet" href="static/test.css">

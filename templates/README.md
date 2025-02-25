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

### `extract.html` (JavaScript Concepts)

- DOM Manipulation (`document.getElementById()`, `.src`, `.style.display`)
- Event Handling (`.then()`, `.catch()`)
- Basic Fetch API (`fetch(url, { method: "POST", body: formData })`)
- Media APIs (`navigator.mediaDevices.getUserMedia()` → Captures webcam video)
- Canvas API (`canvas.toBlob()` → Converts an image for upload)
- FormData API (`new FormData()` → Sends files to the backend)
- Blob & Binary Handling (`new Blob()`, `Uint8Array()`)

### Process of Image Processing
- upload an image this is in image bytes and convert it to byes to be sent to the server.
- Then in the backend it is converted again to image byte to be processed by the YOLO model.
- After the process it is converted again to bytes to be sent to the front-end.
- lastly the front end will convert this into a displayable image.
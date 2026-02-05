# Jinja Template GUI Tool

A graphical user interface tool built with tkinter for processing Jinja2 template files.

## 🌍 Internationalization Support

This tool now supports internationalization in 7 languages:
- Simplified Chinese (Default)
- English
- Japanese
- Korean
- German
- French
- Italian

Switch languages through the "Language" option in the top menu bar.

## Features

- 🖥️ Intuitive graphical interface operation
- 📁 Support for selecting Jinja2 template files (.j2, .tpl, .tmpl formats)
- 📝 Dual-mode data input (form input and JSON input)
- 🔍 Automatic template variable detection
- 👁️ Real-time preview of generated results
- 💾 Result saving functionality
- 🔄 Template hot reloading

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python main.py
```

## Interface Overview

### 1. Template Selection Area
- **Select File**: Browse and select Jinja2 template files
- **Reload**: Reload the current template file
- Display the currently selected file name

### 2. Data Input Area
Two data input methods are provided:

**Form Input Tab**:
- Automatically detects variables in the template
- Generates input fields for each variable
- Supports automatic type conversion (numbers, booleans, lists, etc.)

**JSON Input Tab**:
- Direct input of JSON formatted data
- Suitable for complex data structures
- Real-time syntax validation

### 3. Result Display Area
- Real-time display of generated text results
- Scrollable view for long texts
- Syntax-highlighted friendly display

### 4. Action Buttons
- **Generate Text**: Render template based on input data
- **Save Result**: Save generated results to file
- **Clear All**: Clear all inputs and results

## Template Syntax Support

Supports standard Jinja2 syntax and special functions:

### Variable Substitution
```jinja2
Hello {{ name }}!
Your age is {{ age }} years.
```

### Conditional Statements
```jinja2
{% if age >= 18 %}
Adult
{% else %}
Minor
{% endif %}
```

### Loop Statements
```jinja2
<ul>
{% for item in items %}
<li>{{ item }}</li>
{% endfor %}
</ul>
```

### Special Function Support
```jinja2
{# Exception handling function #}
{{ raise_exception("Error message") }}

{# String processing functions #}
{{ text | trim }}
```

### Complex Template Examples
The tool supports complex chat templates like `chat_template.jinja`, including:
- Multi-language support
- Role alternation validation
- Content type handling (text/image)
- Strict format validation

## Example Templates

The project includes two example templates:

1. `test_template.html.j2` - HTML resume template
2. `resume_template.txt.j2` - Text resume template

## Configuration File

The program automatically generates a `config.json` configuration file that stores:
- Recently used templates
- Window size settings
- Font size
- Last used variable values

## Error Handling

- Template syntax error notifications
- JSON format validation
- File read/write exception handling
- User-friendly error messages

## Development Information

### Project Structure
```
jinjautil/
├── main.py              # Main program entry point
├── template_processor.py # Core template processing logic
├── i18n.py              # Internationalization manager
├── requirements.txt      # Dependency list
├── README.md            # English documentation
├── README_zh.md         # Chinese documentation
├── config.json          # Unified configuration file
├── locales/             # Translation files directory
│   ├── zh_CN/          # Chinese translations
│   ├── en_US/          # English translations
│   └── ...             # Other language translations
└── example/             # Example template files
    ├── test_template.html.j2
    └── resume_template.txt.j2
```

### Core Components

1. **Main Application (`main.py`)**
   - Tkinter-based GUI implementation
   - Menu system with language switching
   - File selection and template loading
   - Data input handling (both form and JSON)
   - Result display and export functionality

2. **Template Processor (`template_processor.py`)**
   - Jinja2 environment configuration
   - Variable extraction from templates
   - Template rendering with data merging
   - Custom function and filter support

3. **Internationalization (`i18n.py`)**
   - Multi-language support management
   - gettext-based translation system
   - Language switching with runtime updates
   - Configuration persistence

### Dependencies

- **Jinja2** (>=3.1.0): Template engine
- **Babel** (>=2.12.0): Internationalization utilities
- **Python Standard Library**: tkinter, json, os, pathlib

### Adding New Languages

1. Create new language directory: `locales/{language_code}/LC_MESSAGES/`
2. Copy existing `.po` file and translate messages
3. Compile translations: `pybabel compile -d locales`
4. Add language to `SUPPORTED_LANGUAGES` in `i18n.py`

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
6. 
### Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing documentation
- Review example templates for usage patterns
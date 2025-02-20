import os

# Define base templates directory
BASE_DIR = os.path.join(os.getcwd(), "templates")

# Define apps and their template files
TEMPLATES_STRUCTURE = {
    "store": [
        "index.html",
        "ebook_detail.html",
        "audiobook_detail.html",
        "checkout.html",
        "order_success.html"
    ],
    "sermons": [
        "index.html",
        "sermon_detail.html",
        "sermon_archive.html"
    ],
    "blog": [
        "index.html",
        "blog_detail.html",
        "blog_category.html",
        "blog_author.html"
    ],
    "donations": [
        "index.html",
        "give.html",
        "thank_you.html",
        "donation_history.html"
    ],
    "users": [
        "login.html",
        "logout.html",
        "register.html",
        "profile.html",
        "dashboard.html"
    ],
    "common": [
        "base.html",
        "navbar.html",
        "footer.html",
        "home.html"
    ],
    "home": [
        "index.html",
        "about.html",
        "contact.html"
    ],
    "dependencies": [
        "css.html",
        "js.html",
    ]
}

# Default content for files
BASE_HTML_CONTENT = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}JCRM{% endblock %}</title>
    
    <!-- Import Tailwind CSS -->
    {% include 'dependencies/css.html' %}
</head>
<body class="bg-gray-100 text-gray-900">

    {% include 'common/navbar.html' %}

    <div class="container mx-auto mt-10">
        {% block content %}{% endblock %}
    </div>

    {% include 'common/footer.html' %}

    <!-- Import JavaScript -->
    {% include 'dependencies/js.html' %}
</body>
</html>
"""

NAVBAR_HTML_CONTENT = """{% load static %}
<nav class="bg-red-600 text-white p-4">
    <div class="container mx-auto flex justify-between">
        <a href="/" class="font-bold text-lg">JCRM</a>
        <ul class="flex space-x-4">
            <li><a href="{% url 'home:index' %}" class="hover:text-gray-300">Home</a></li>
            <li><a href="{% url 'sermons:index' %}" class="hover:text-gray-300">Sermons</a></li>
            <li><a href="{% url 'store:index' %}" class="hover:text-gray-300">Store</a></li>
            <li><a href="{% url 'donations:index' %}" class="hover:text-gray-300">Give</a></li>
            <li><a href="{% url 'blog:index' %}" class="hover:text-gray-300">Blog</a></li>
        </ul>
    </div>
</nav>
"""

FOOTER_HTML_CONTENT = """{% load static %}
<footer class="bg-black text-white p-6 mt-10 text-center">
    <p>&copy; 2025 JCRM Church. All rights reserved.</p>
</footer>
"""

CSS_HTML_CONTENT = """{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">
"""

JS_HTML_CONTENT = """{% load static %}
<script src="{% static 'js/index.js' %}" defer></script>
"""

DEFAULT_PAGE_CONTENT = """{% extends 'common/base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="text-center py-10">
    <h1 class="text-3xl font-bold">Welcome to {page_name}</h1>
</div>
{% endblock %}
"""

def create_templates():
    """Creates folders and template files for Django project."""
    for app, files in TEMPLATES_STRUCTURE.items():
        app_dir = os.path.join(BASE_DIR, app)
        os.makedirs(app_dir, exist_ok=True)

        for file in files:
            file_path = os.path.join(app_dir, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    if file == "base.html":
                        f.write(BASE_HTML_CONTENT)
                    elif file == "navbar.html":
                        f.write(NAVBAR_HTML_CONTENT)
                    elif file == "footer.html":
                        f.write(FOOTER_HTML_CONTENT)
                    elif file == "css.html":
                        f.write(CSS_HTML_CONTENT)
                    elif file == "js.html":
                        f.write(JS_HTML_CONTENT)
                    else:
                        f.write(DEFAULT_PAGE_CONTENT.replace("{page_name}", file.replace('.html', '').title()))

                print(f"✅ Created: {file_path}")
            else:
                print(f"⚡ Exists: {file_path}")

if __name__ == "__main__":
    create_templates()
    print("\n🎉 Template structure created successfully!")

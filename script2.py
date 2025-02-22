import os

# Define project and app names
project_name = "jcrm"
apps = [
    "home", "about", "watch", "read", "listen", "ministries", "events", "store", "blog", "contact", "account", "requests", "donations"
]

def create_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def create_file(path, content=""):
    """Create file with content if it doesn't exist."""
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

# Set up global templates
global_templates_dir = os.path.join(project_name, "templates")
create_directory(global_templates_dir)
global_template_files = ["base.html", "navbar.html", "footer.html"]
for file in global_template_files:
    create_file(os.path.join(global_templates_dir, file), f"<!-- {file} global template -->")

# Iterate over each app to create directories, files, and basic structure
for app in apps:
    app_dir = os.path.join(project_name, app)
    templates_dir = os.path.join(app_dir, "templates", app)
    
    # Create necessary directories
    create_directory(app_dir)
    create_directory(templates_dir)
    
    # Create empty __init__.py to make it a package
    create_file(os.path.join(app_dir, "__init__.py"))
    
    # Create urls.py with basic structure
    urls_content = f"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='{app}_index'),
]
"""
    create_file(os.path.join(app_dir, "urls.py"), urls_content.strip())
    
    # Create views.py with a basic function
    views_content = f"""
from django.shortcuts import render

def index(request):
    return render(request, '{app}/index.html')
"""
    create_file(os.path.join(app_dir, "views.py"), views_content.strip())
    
    # Create empty template file for the app
    create_file(os.path.join(templates_dir, "index.html"), f"<!-- {app} Page Template -->")

print("✅ All apps, URLs, views, and templates have been set up successfully!")

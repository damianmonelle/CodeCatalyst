def get_app_templates():
    """
    Provide pre-defined file structure templates for different app types categorized by use case.

    Returns:
        dict: A dictionary containing categories and their respective templates.
    """
    templates = {
        "Mobile": {
            "android": {
                "project_root": "AndroidApp",
                "folders": [
                    "app/src/main/java/com/example",
                    "app/src/main/res/layout",
                    "app/src/main/res/drawable",
                    "app/src/main/res/values",
                    "app/src/main/assets",
                    "app/src/test/java/com/example",
                    "app/src/androidTest/java/com/example"
                ],
                "files": {
                    "": ["README.md", "build.gradle"],
                    "app/src/main/java/com/example": ["MainActivity.java"],
                    "app/src/main/res/layout": ["activity_main.xml"],
                    "app/src/main/res/drawable": ["ic_launcher.png"],
                    "app/src/main/res/values": ["strings.xml", "colors.xml"],
                    "app/src/main/assets": ["config.json"],
                    "app/src/test/java/com/example": ["MainActivityTest.java"],
                    "app/src/androidTest/java/com/example": ["UITest.java"]
                }
            },
            "flutter": {
                "project_root": "FlutterApp",
                "folders": [
                    "lib",
                    "assets/images",
                    "assets/fonts",
                    "test"
                ],
                "files": {
                    "": ["README.md", "pubspec.yaml"],
                    "lib": ["main.dart", "home.dart", "utils.dart"],
                    "assets/images": ["logo.png"],
                    "assets/fonts": ["Roboto-Regular.ttf"],
                    "test": ["widget_test.dart"]
                }
            }
        },
        "Python": {
            "basic_script": {
                "project_root": "BasicPythonScript",
                "folders": ["src", "tests", "docs"],
                "files": {
                    "": ["README.md", "main.py", ".gitignore", "requirements.txt"],
                    "src": ["utils.py"],
                    "tests": ["test_main.py"],
                    "docs": ["CHANGELOG.md"]
                }
            },
            "flask_app": {
                "project_root": "FlaskApp",
                "folders": ["app/templates", "app/static/css", "app/static/js", "app/static/images", "tests", "configs"],
                "files": {
                    "": ["README.md", "app.py", "requirements.txt", ".gitignore"],
                    "app/templates": ["index.html", "layout.html"],
                    "app/static/css": ["styles.css"],
                    "app/static/js": ["app.js"],
                    "app/static/images": [],
                    "tests": ["test_app.py"],
                    "configs": ["config.py"]
                }
            },
            "django_app": {
                "project_root": "DjangoApp",
                "folders": ["myapp/templates", "myapp/static/css", "myapp/static/js", "myapp/static/images", "configs", "tests"],
                "files": {
                    "": ["README.md", "manage.py", "requirements.txt", ".gitignore"],
                    "myapp/templates": ["index.html"],
                    "myapp/static/css": ["styles.css"],
                    "myapp/static/js": ["app.js"],
                    "myapp/static/images": [],
                    "configs": ["settings.py"],
                    "tests": ["test_views.py"]
                }
            },
            "fastapi_app": {
                "project_root": "FastAPIApp",
                "folders": ["app/routes", "app/models", "app/services", "configs", "tests"],
                "files": {
                    "": ["README.md", "main.py", "requirements.txt", ".gitignore"],
                    "app/routes": ["user_routes.py"],
                    "app/models": ["user_model.py"],
                    "app/services": ["user_service.py"],
                    "configs": ["settings.py"],
                    "tests": ["test_routes.py"]
                }
            },
            "pyqt_gui": {
                "project_root": "PyQtApp",
                "folders": ["src", "resources/icons", "configs", "tests"],
                "files": {
                    "": ["README.md", "main.py", "requirements.txt", ".gitignore"],
                    "src": ["main_window.py", "app_logic.py"],
                    "resources/icons": ["app_icon.png"],
                    "configs": ["settings.json"],
                    "tests": ["test_gui.py"]
                }
            }
        },
        "Frontend": {
            "web": {
                "project_root": "WebApp",
                "folders": [
                    "public",
                    "src/components",
                    "src/services",
                    "assets/css",
                    "assets/js",
                    "assets/images"
                ],
                "files": {
                    "": ["README.md", "package.json", ".gitignore"],
                    "public": ["index.html", "favicon.ico"],
                    "src": ["App.js", "index.js"],
                    "src/components": ["Header.js", "Footer.js"],
                    "src/services": ["api.js"],
                    "assets/css": ["styles.css", "reset.css"],
                    "assets/js": ["utils.js"],
                    "assets/images": ["logo.png"]
                }
            }
        },
        "Backend": {
            "api_service": {
                "project_root": "APIService",
                "folders": [
                    "src/routes",
                    "src/models",
                    "src/controllers",
                    "tests",
                    "configs",
                    "docs"
                ],
                "files": {
                    "": ["README.md", "app.py", ".gitignore"],
                    "src/routes": ["index.py", "user_routes.py"],
                    "src/models": ["user_model.py"],
                    "src/controllers": ["user_controller.py"],
                    "tests": ["test_routes.py", "test_models.py"],
                    "configs": ["config.yaml"],
                    "docs": ["API_DOCS.md", "CHANGELOG.md"]
                }
            }
        }
    }

    return templates

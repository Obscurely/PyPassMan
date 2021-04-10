import os
import platform

# Checks the platform and based on it assigns the platform_separator
if platform.system() == "Windows":
    platform_separator = "\\"
else:
    platform_separator = "/"


def load_current_style():
    """
    Returns the name of the current style name in use.

    :return: Current style name.
    """
    file_name = "PyPassMan_Files" + platform_separator + "current_style.qss"
    with open(file_name, "r") as f:
        current_style = f.read()
    return current_style


def get_stylesheets():
    """
    Gets a list with all the available styles for the app.

    :return: List with style sheets.
    """
    current_dir = os.getcwd()
    os.chdir("PyPassMan_Files" + platform_separator + "QtStyles")

    all_files = os.listdir()
    stylesheets_list = []
    for file in all_files:
        file = file.removesuffix(".qss")
        if ".qss" not in file:
            stylesheets_list.append(file)

    os.chdir(current_dir)
    return stylesheets_list


def change_current_style(stylesheet_file: str):
    """
    Changes the style of the app to given style name.

    :param stylesheet_file: The name of the style.
    :return: Returns return "changed current style" if style was changed.
    """
    file_name = (
        "PyPassMan_Files"
        + platform_separator
        + "QtStyles"
        + platform_separator
        + stylesheet_file
    )
    with open(file_name, "r") as f:
        new_style = f.read()
    file_name = "PyPassMan_Files" + platform_separator + "current_style.qss"
    with open(file_name, "w") as f:
        f.write(new_style)
    return "changed current style"


def add_style_sheet(stylesheet_name: str, stylesheet_text: str):
    """
    Adds a new style to that app with the given name and content.

    :param stylesheet_name: the name of the new style sheet.
    :param stylesheet_text: the content of the new style sheet.
    :return: Returns "style added" if the style was added.
    """
    file_name = (
        "PyPassMan_Files"
        + platform_separator
        + "QtStyles"
        + platform_separator
        + stylesheet_name
        + ".qss"
    )
    with open(file_name, "w") as f:
        f.write(stylesheet_text)
    return "style added"

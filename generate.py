#!.venv/bin/python3
import os
import json
import re
import shutil
from pathlib import Path

directory = os.path.dirname(os.path.realpath(__file__))

# https://regex101.com/r/UUNGtd/1
regex = r'(:)\s*((((\w+)(\.))?(%s))|((")(%s)("))|((\')(%s)(\')))\s*(=)\s*(\\)?\s*([bBrRuU]?f?)("{3})'
#        ^      ^    ^     ^      ^  ^   ^     ^   ^   ^           ^     ^        ^           ^
#        1      5    6     7      9  10  11    13  14  15         16     17       18          19

begin_captures = {
    "1": {"name": "punctuation.separator.colon.python"},
    "5": {"name": "source.python"},
    "6": {"name": "punctuation.separator.period.python"},
    "7": {"name": "meta.attribute.python"},
    "9": {"name": "string.quoted.single.python"},
    "10": {"name": "string.quoted.single.python"},
    "11": {"name": "string.quoted.single.python"},
    "13": {"name": "string.quoted.single.python"},
    "14": {"name": "string.quoted.single.python"},
    "15": {"name": "string.quoted.single.python"},
    "16": {"name": "keyword.operator.assignment.python"},
    "17": {"name": "source.python"},
    "18": {"name": "storage.type.string.python"},
    "19": {"name": "string.quoted.multi.python"},     
}


def make_vs_code_extension(languages):
    package_file_path = os.path.join(
        directory, "vscode-python-inline-source", "package.json"
    )
    readme_file_path = os.path.join(
        directory, "README.md"
    )
    add_supported_languages_to_readme(languages, readme_file_path)
    syntax_file_path = os.path.join(
        directory,
        "vscode-python-inline-source",
        "syntaxes",
        "python-inline-source.json",
    )
    with open(package_file_path, "r") as f:
        package = json.load(f)
    with open(syntax_file_path, "r") as f:
        syntax = json.load(f)
    embedded_languages = {}
    patterns = []
    for langname, options in languages.items():
        embedded_languages[options["contentName"]] = langname
        pattern = {   
                "name": "meta.embedded.container.python",
                "contentName": options["contentName"],
                "begin": regex % ((options["match"],) * 3),
                "beginCaptures": begin_captures,
                "end": '("{3})',
                "endCaptures": {"1": {"name": "string.quoted.multi.python"}},
                "patterns": [{"include": options["include"]}],
                "applyEndPatternLast":0
            }
        #pattern["begin"] = pattern["begin"].replace("\\'", "'")
        #pattern["begin"] = pattern["end"].replace("\\'", "'")
        patterns.append(pattern)
    package["contributes"]["grammars"][0]["embeddedLanguages"] = embedded_languages
    syntax["patterns"] = patterns
    with open(package_file_path, 'w') as f:
        json.dump(package, f, indent=4)
    with open(syntax_file_path, 'w') as f:
        json.dump(syntax, f, indent=4)


def make_python_types(languages):
    sourcetypes_file_path = os.path.join(
        directory, "sourcetypes/sourcetypes", "__init__.py"
    )
    readme_file_path = os.path.join(
        directory, "README.md"
    )
    add_supported_languages_to_readme(languages, readme_file_path)
    with open(sourcetypes_file_path, 'w') as f:
        f.writelines(
            [
                "try:\n",
                "    from typing import Annotated\n",
                "except ImportError:\n",
                "    from typing_extensions import Annotated\n",
                "\n",
                "source_code = Annotated[str, 'source_code']\n",
                "\n",
            ]
        )
        for langname, options in languages.items():
            f.write(f"{langname} = Annotated[source_code, '{langname}']\n")
            for alias in options["match"].split("|"):
                if alias != langname:
                    f.write(f"{alias} = {langname}\n")
            f.write("\n")


def add_supported_languages_to_readme(languages, readme_file_path):
    with open(readme_file_path, "r") as f:
        readme = f.read()
    
    readme_text = []
    for langname, options in languages.items():
        readme_text_line = f"\n- `{langname}`"
        aliases = [f"`{m}`" for m in options['match'].split("|") if m != langname]
        if aliases:
            if len(aliases) > 1:
                aliases[-1] = f"and {aliases[-1]}"
            readme_text_line = f"{readme_text_line} (aliased as {', '.join(aliases)})"
        readme_text.append(readme_text_line)
    
    new_languages_section = f"## Supported Languages\n{''.join(readme_text)}\n"
    
    readme = re.sub(r"(## Supported Languages\n)(.*?)(?=\n# Release Notes|\n## Building|\Z)", fr"\1{''.join(readme_text)}\n", readme, flags=re.DOTALL)
    
    with open(readme_file_path, 'w') as f:
        f.write(readme)
    
    


def main():
    with open(os.path.join(directory, "languages.json"), "r") as f:
        languages = json.load(f)
    make_vs_code_extension(languages)
    make_python_types(languages)
    add_supported_languages_to_readme(languages, os.path.join(directory, "README.md"))
    _dir = Path(directory)
    README=_dir.joinpath("README.md")
    shutil.copy2(README,_dir.joinpath("vscode-python-inline-source/README.md"))
    shutil.copy2(README,_dir.joinpath("sourcetypes/README.md"))

    shutil.copy2(_dir.joinpath("requirements.txt"),_dir.joinpath("sourcetypes/requirements.txt"))

    DOCS=_dir.joinpath("docs")
    shutil.copytree(DOCS, _dir.joinpath("sourcetypes/docs"), dirs_exist_ok=True)
    shutil.copytree(DOCS, _dir.joinpath("vscode-python-inline-source/docs"), dirs_exist_ok=True)


if __name__ == "__main__":
    main()

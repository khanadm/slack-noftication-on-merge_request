import argparse
import datetime
import subprocess

import packaging.version

from build_utils import extract_variable_value, replace_variable_value


def main(src_file: str):
    with open(src_file) as f:
        src_content = f.read()

    version = extract_variable_value(src_content, "__version__")  # e.g  1.2.3
    packaging.version.Version(version)  # will raise for invalid python version
    git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    date = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

    new_content = replace_variable_value(src_content, "__commit__", f'"{git_hash}"')
    new_content = replace_variable_value(new_content, "__date__", f'"{date}"')
    new_content = replace_variable_value(new_content, "__semver__", f'"{version}+{date}.{git_hash}"')

    with open(src_file, "w") as f:
        f.write(new_content)

    print(version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update build info into a project source file")
    parser.add_argument("src_file", type=str, help="Python file containing __version__, __commit__, __date__ variables")
    args = parser.parse_args()
    main(args.src_file)

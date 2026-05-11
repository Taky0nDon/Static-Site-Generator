import os

from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(template_path) as f:
        template = f.read()

    walker = os.walk(from_path)
    try:
        while walking := next(walker):
            new_dir = ''
            dirpath, dirnames, filenames = walking
            print(f"{dirpath=}")
            print(f"{dirnames=}")
            abs_dirpath = os.path.abspath(dirpath)
            dst_dir = os.path.join(dest_path, dirpath)
            print(f"Checking for {dst_dir}")
            if not os.path.exists(dst_dir):
                print(f"Creating {new_dir}")

                os.mkdir(os.path.join(dest_path, dirpath))
            print(f"Filenames: {filenames}")
            for file in filenames:
                new_filename = ".".join([os.path.splitext(file)[0], "html"])
                abs_file_path = os.path.abspath(os.path.join(dirpath, file))
                print(f"Opening {abs_file_path}")

                with open(abs_file_path) as f:
                    md_file = f.read()

                title = extract_title(md_file)
                node = markdown_to_html_node(md_file)
                html = node.to_html()
                print(f"Extracting title from {abs_file_path}")

                new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

                if os.path.split(dirpath)[-1] == "content":
                    new_file_path = os.path.join(dest_path, new_filename)
                    print("HERE: ", new_file_path)
                else:
                    new_dir = os.path.join(dirpath.split("content/")[-1])
                    to_create = ""
                    for part in os.path.split(new_dir):
                        to_create = os.path.join(to_create, part)
                        print(to_create)
                        new_public_dir = os.path.join(dest_path, to_create)
                        if not os.path.exists(new_public_dir):
                            print(f"Creating {new_public_dir=}")
                            os.mkdir(new_public_dir)
                    print(f"{dest_path=}")
                    new_file_path = os.path.join(dest_path, new_dir, new_filename)

                print(f"{dirpath=}")
                print(f"{new_dir=}")
                print(f"{dest_path=}")
                print(f"{dirpath=}")
                print(f"writing {new_file_path}")
                if os.path.exists(new_file_path):
                    print(f"{new_file_path} exists!")
                with open(new_file_path, "w") as out_file:
                    out_file.write(new_html)
    except StopIteration as e:
        return





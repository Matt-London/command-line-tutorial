from ..filesystem.Directory import Directory
from ..resources.colors import colors
from ..filesystem.File import File

import os


class Commands:

    @staticmethod
    def ls(directory):
        if not (type(directory) is Directory):
            raise ValueError("'directory' argument must be Directory, found %s" % type(directory))

        contents = list(directory.contents)
        contents.sort(key=lambda x: x.name)

        width, height = -1, -1
        try:
            size = os.get_terminal_size()
            width = size.columns
            height = size.lines
        except OSError:
            pass

        has_dimensions = width > -1 and height > -1

        if has_dimensions:
            rough_width = len(" ".join(contents))
            rough_height = rough_width//width
            rough_width %= width

            lines = []
            for i in range(rough_height):
                line = []
                index = i
                while index < rough_width and index < len(contents):
                    item = contents[index]
                    name = item.name
                    if type(item) is Directory:
                        name = colors.fg.blue + name
                    line.append(name)
                    index += 1
                lines.append(line)
            for line in lines:
                print(*line)
        else:
            for item in contents:
                if type(item) is Directory:
                    print(colors.fg.blue, end="")

                print(item.name + colors.reset)

        if contents and has_dimensions:
            print()

import optparse
import sys

import transformation
import visualizing


def main():
    parser = optparse.OptionParser(usage="astvisualizer.py [options] [string]")
    parser.add_option("-f", "--file", action="store",
                      help="Read a code snippet from the specified file")

    options, _ = parser.parse_args(sys.argv)
    if options.file:
        with open(options.file) as input_file:
            code = input_file.read()

            label = options.file

            transformed_ast = transformation.get_transformed_ast(code)

            renderer = visualizing.GraphRenderer()
            renderer.render(transformed_ast, label=label)

    else:
        print("No input file")


if __name__ == '__main__':
    main()

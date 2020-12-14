import transformation
import visualizing


def main():
    input_file = 'tests/1_simple_if_else_test.py'
    with open(input_file) as input_fp:
        code = input_fp.read()

        transformed_ast = transformation.get_transformed_ast(code)

        renderer = visualizing.GraphRenderer()
        renderer.render(data=transformed_ast, file_name=input_file[:-3], label=input_file)


if __name__ == '__main__':
    main()

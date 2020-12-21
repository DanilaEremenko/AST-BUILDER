import transformation, visualizing


def main():
    input_file = 'tests/1_assign.py'
    with open(input_file) as input_fp:
        code = input_fp.read()

        transformed_ast = transformation.get_transformed_ast(code)

        renderer = visualizing.GraphRenderer()
        renderer.render(data=transformed_ast, file_name='py_native_result', label=input_file)


if __name__ == '__main__':
    main()

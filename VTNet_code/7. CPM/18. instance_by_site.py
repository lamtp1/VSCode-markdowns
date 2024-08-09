def print_matching_lines(file_path, input_strings, output_file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(input_strings, 'r') as f:
        search_strings = f.readlines()

    matching_lines = [line for line in lines for search_string in search_strings if search_string.strip() in line]

    with open(output_file_path, 'w') as f:
        f.writelines(matching_lines)

file_path = "Vật lý.txt"
input_strings = "search_strings.txt"
output_file_path = "output.txt"
print_matching_lines(file_path, input_strings, output_file_path)

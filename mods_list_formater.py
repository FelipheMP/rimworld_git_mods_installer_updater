def format_mod_text(mod_text):
    mod_name, url = mod_text.split(" ")
    
    formatted_mod = f'    ("{mod_name}", "{url}"),'
    
    return formatted_mod

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # Sort lines alphabetically by mod name
    sorted_lines = sorted(lines, key=lambda line: line.split(" ")[0].lower())

    formatted_lines = [format_mod_text(line.strip()) for line in sorted_lines]
    
    with open(output_file_path, 'w') as file:
        file.write('mods = [\n')
        file.write('\n'.join(formatted_lines))
        file.write('\n]\n')

def sorting_modslist_txt(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # Sort lines alphabetically by mod name
    sorted_lines = sorted(lines, key=lambda line: line.split(" ")[0].lower())
    
    with open(input_file_path, 'w') as file:
        file.writelines(sorted_lines)

if __name__ == "__main__":
    input_file_path = 'mods_list.txt'
    output_file_path = 'mods_list.py'
    process_file(input_file_path, output_file_path)

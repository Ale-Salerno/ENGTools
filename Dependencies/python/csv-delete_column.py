import os
import csv
import string

def excel_col_to_index(col_str):
    """Converts an Excel-style column letter to a 0-based index."""
    col_str = col_str.upper()
    index = 0
    for char in col_str:
        index = index * 26 + (ord(char) - ord('A') + 1)
    return index - 1

def delete_column_from_csv(input_folder, output_folder, delimiter_input, column_to_delete_input):
    """
    Deletes a specified column from CSV files within a folder and its subfolders.

    Args:
        input_folder (str): The path to the input folder containing CSV files.
        output_folder (str): The path to the output folder where modified CSV files will be saved.
        delimiter_input (str): User input for the delimiter.
        column_to_delete_input (str): User input for the column to delete (letter or index).
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)

                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                try:
                    with open(input_path, 'r', newline='', encoding='utf-8') as infile, \
                         open(output_path, 'w', newline='', encoding='utf-8') as outfile:

                        if delimiter_input.lower() == "tab":
                            reader = csv.reader(infile, dialect=csv.excel_tab)
                            writer = csv.writer(outfile, dialect=csv.excel_tab, quoting=csv.QUOTE_MINIMAL)
                        elif delimiter_input == " ":
                            reader = csv.reader(infile, delimiter=" ")
                            writer = csv.writer(outfile, delimiter=" ", quoting=csv.QUOTE_MINIMAL)
                        else:
                            reader = csv.reader(infile, delimiter=delimiter_input)
                            writer = csv.writer(outfile, delimiter=delimiter_input, quoting=csv.QUOTE_MINIMAL)

                        try:
                            column_to_delete = int(column_to_delete_input) #try to convert directly to integer
                        except ValueError:
                            column_to_delete = excel_col_to_index(column_to_delete_input) #If it fails, it means it is a letter column.
                        for row in reader:
                            if len(row) > column_to_delete:
                                new_row = [row[i] for i in range(len(row)) if i != column_to_delete]
                                writer.writerow(new_row)
                            else:
                                writer.writerow(row)
                except Exception as e:
                    print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    input_folder = "i"
    output_folder = "o"

    delimiter_input = input("Enter the CSV delimiter (e.g., ;, comma, tab, space): ")
    column_to_delete_input = input("Enter the column to delete (e.g., A, B, 0, 1): ")

    delete_column_from_csv(input_folder, output_folder, delimiter_input, column_to_delete_input)
    print(f"Column {column_to_delete_input} deleted from CSV files in '{input_folder}' and saved to '{output_folder}'.")
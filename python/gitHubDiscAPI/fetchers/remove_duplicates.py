def remove_duplicate_lines(input_file, output_file):
    unique_lines = set()  # Set to store unique lines
    
    # Read input file and store unique lines in the set
    with open(input_file, "r") as file:
        for line in file:
            unique_lines.add(line.strip())
    
    # Write unique lines back to the output file
    with open(output_file, "w") as file:
        for line in unique_lines:
            file.write(line + "\n")

if __name__ == "__main__":
    input_file = "top_repositories_2024.txt"
    output_file = "repository_names_unique.txt"
    
    remove_duplicate_lines(input_file, output_file)
    print("Duplicate lines removed. Unique lines saved to 'repository_names_unique.txt'")

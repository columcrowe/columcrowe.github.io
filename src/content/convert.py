import pypandoc
from pathlib import Path
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Convert DOCX to Markdown using pypandoc')
parser.add_argument('input_file', type=str, help='Path to the .docx file')

args = parser.parse_args()

# Convert
input_path = Path(args.input_file)
output_path = input_path.with_suffix('.md')

pypandoc.convert_file(input_path, 'md', outputfile=str(output_path))
print(f"Converted '{input_path}' to '{output_path}'")

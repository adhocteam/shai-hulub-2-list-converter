import csv
import sys
import argparse
import os

def parse_txt_line(line):
    """
    Parses a line in the format 'package@version'.
    Handles scoped packages (e.g., @scope/pkg@1.2.3).
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    
    # Split from the right to handle scoped packages starting with @
    try:
        package, version = line.rsplit('@', 1)
        return package, version
    except ValueError:
        # Fallback if no version is specified or format is weird
        return line, "UNKNOWN"

def txt_to_csv(input_file, output_file):
    """Converts a TXT file of package@version to a CSV file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', newline='', encoding='utf-8') as f_out:
            
            writer = csv.writer(f_out)
            writer.writerow(['package', 'version'])  # Write Header
            
            count = 0
            for line in f_in:
                result = parse_txt_line(line)
                if result:
                    writer.writerow(result)
                    count += 1
            
            print(f"Success: Converted {count} entries from TXT to CSV.")
            print(f"Output saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def csv_to_txt(input_file, output_file):
    """Converts a CSV file (cols: package, version) to a TXT file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            
            reader = csv.reader(f_in)
            
            # Attempt to handle header
            try:
                header = next(reader)
                # If the first row looks like a package (contains . or - or @), it might not be a header.
                # But standard CSVs usually have headers. We assume standard 'package, version' header exists.
                # If the header doesn't match expected strings, we reset (seek 0) if strictly needed, 
                # but for this tool, we assume a header row exists if it looks like text.
                if header[0].lower() not in ['package', 'name', 'library', 'indicator']:
                    # If it doesn't look like a header, process it as data
                    if len(header) >= 2:
                        f_out.write(f"{header[0]}@{header[1]}\n")
            except StopIteration:
                pass # Empty file

            count = 0
            for row in reader:
                if len(row) >= 2:
                    pkg = row[0].strip()
                    ver = row[1].strip()
                    f_out.write(f"{pkg}@{ver}\n")
                    count += 1
            
            print(f"Success: Converted {count} entries from CSV to TXT.")
            print(f"Output saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Convert Shai-Hulud 2.0 vulnerability lists between TXT and CSV formats."
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument(
        "-to-txt", 
        action="store_true", 
        help="Flag to convert FROM CSV TO TXT. Default is TXT TO CSV."
    )

    args = parser.parse_args()

    if args.to_txt:
        csv_to_txt(args.input_file, args.output_file)
    else:
        txt_to_csv(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

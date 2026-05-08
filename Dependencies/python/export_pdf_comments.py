import fitz # PyMuPDF
import pandas as pd
import os
from datetime import datetime

def export_pdf_comments():
    """
    Exports comments (annotations) from all PDF files in the running directory
    to individual CSV and Excel files.
    """
    current_directory = os.getcwd()
    pdf_files_found = False

    print(f"Searching for PDF files in: {current_directory}")

    # Iterate through all files in the current directory
    for filename in os.listdir(current_directory):
        # Check if the file is a PDF (case-insensitive)
        if filename.lower().endswith(".pdf"):
            pdf_files_found = True
            pdf_path = os.path.join(current_directory, filename)

            # Generate output filenames based on the current PDF's name
            base_name = os.path.splitext(filename)[0]
            output_csv_path = os.path.join(current_directory, f"{base_name}_comments.csv")
            output_excel_path = os.path.join(current_directory, f"{base_name}_comments.xlsx")

            comments_data = [] # List to store dictionaries of comment information for the current PDF

            try:
                doc = fitz.open(pdf_path)
                print(f"\nProcessing '{filename}'...")

                # Iterate through each page of the PDF document
                for page_num, page in enumerate(doc):
                    # Iterate through each annotation (comment) on the current page
                    for annot in page.annots():
                        # Get the annotation subtype string, which is more reliable
                        # e.g., "/Text", "/Highlight", "/StrikeOut"
                        subtype = annot.info.get("subtype", "").strip()
                        comment_type = "Unknown Type" # Default fallback

                        # Map common subtypes to readable names
                        if subtype == "/Text":
                            comment_type = "Sticky Note"
                        elif subtype == "/Highlight":
                            comment_type = "Highlight"
                        elif subtype == "/Underline":
                            comment_type = "Underline"
                        elif subtype == "/Squiggly":
                            comment_type = "Squiggly Underline"
                        elif subtype == "/StrikeOut":
                            comment_type = "Strikeout"
                        elif subtype == "/FreeText":
                            comment_type = "Text Box"
                        elif subtype == "/Line":
                            comment_type = "Line"
                        elif subtype == "/Square":
                            comment_type = "Rectangle"
                        elif subtype == "/Circle":
                            comment_type = "Circle"
                        elif subtype == "/Polygon":
                            comment_type = "Polygon"
                        elif subtype == "/PolyLine":
                            comment_type = "Polyline"
                        elif subtype == "/Ink":
                            comment_type = "Ink Annotation (Drawing)"
                        elif subtype == "/Stamp":
                            comment_type = "Stamp"
                        else:
                            comment_type = f"Unknown Type ({subtype})" # Fallback for unhandled types or unexpected subtype strings

                        # Extract the actual comment text, author, and modification date
                        # .get() is used to safely access dictionary keys, providing an empty string if not found
                        comment_text = annot.info.get("content", "").strip()
                        author = annot.info.get("author", "N/A").strip()
                        mod_date_str = annot.info.get("modDate", "").strip()

                        # Parse the date string from "D:YYYYMMDDHHMMSSZ" format to a more readable format
                        parsed_date = "N/A"
                        if mod_date_str and mod_date_str.startswith("D:"):
                            try:
                                # Remove "D:" prefix and "Z" suffix (if present) before parsing
                                date_part = mod_date_str[2:].split('Z')[0]
                                parsed_date = datetime.strptime(date_part, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                # If date parsing fails, keep the original string
                                parsed_date = mod_date_str

                        # Only add comments that have actual text content to the list
                        if comment_text:
                            comments_data.append({
                                "Page": page_num + 1, # Page numbers in PDF are 1-based
                                "Type": comment_type,
                                "Author": author,
                                "Date": parsed_date,
                                "Comment Text": comment_text
                            })
                doc.close() # Close the PDF document after processing

                # If no comments with text content were found for the current PDF
                if not comments_data:
                    print(f"No text-based comments found in '{filename}'. Skipping output file creation for this PDF.")
                else:
                    # Create a Pandas DataFrame from the collected comments data
                    df = pd.DataFrame(comments_data)

                    # Save the DataFrame to a CSV file
                    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
                    print(f"Comments successfully exported to CSV: '{output_csv_path}'")

                    # Save the DataFrame to an Excel file
                    df.to_excel(output_excel_path, index=False)
                    print(f"Comments successfully exported to Excel: '{output_excel_path}'")

            except fitz.EmptyFileError:
                print(f"Error: PDF file '{filename}' is empty or corrupted. Skipping.")
            except Exception as e:
                print(f"An unexpected error occurred while processing '{filename}': {e}. Skipping.")

    if not pdf_files_found:
        print("\nNo PDF files found in the current directory.")
        print("Please ensure your PDF documents are in the same directory as this script.")
    else:
        print("\nAll detected PDF files processed.")

# This ensures the function runs when the script is executed
if __name__ == "__main__":
    export_pdf_comments()

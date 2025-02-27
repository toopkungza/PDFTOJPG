# PDF Extractor

A high-performance Python utility for converting PDF documents to high-quality JPEG images using multiprocessing.

## Features

- Extract single pages or entire PDF documents to JPEG format
- Parallel processing for faster conversion of multi-page documents
- Configurable image quality and scaling
- Simple API for both programmatic and command-line usage
- Comprehensive logging

## Installation

### Prerequisites

- Python 3.6+
- Required packages:
  - pypdfium2
  - pillow (PIL)

### Install with pip

```bash
pip install -r requirements.txt
```

## Usage

### As a Python Module

```python
from main_multiprocessing import extract_pdf_pages

# Extract only the first page of a PDF
first_page_images = extract_pdf_pages("path/to/document.pdf")

# Extract all pages of a PDF with custom settings
all_page_images = extract_pdf_pages(
    pdf_path="path/to/document.pdf",
    output_dir="output/directory",  # Optional: defaults to PDF location
    scale=4,                        # Optional: rendering scale factor
    extract_all=True,               # Extract all pages instead of just first page
    max_workers=4                   # Optional: limit number of parallel processes
)
```

### Advanced Usage - PDFExtractor Class

```python
import logging
from main_multiprocessing import PDFExtractor

# Create extractor with DEBUG logging level
extractor = PDFExtractor(log_level=logging.DEBUG)

# Extract all pages with custom settings
extracted_images = extractor.extract_pdf_pages(
    pdf_path="path/to/document.pdf",
    output_dir="output/directory",
    scale=2,
    extract_all=True,
    max_workers=8
)
```

## Function Parameters

### extract_pdf_pages()

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| pdf_path | str | (Required) | Path to the PDF file |
| output_dir | str | None | Directory to save extracted images. If None, uses the PDF location |
| scale | int | 4 | Rendering scale factor. Higher values produce larger, higher-quality images |
| extract_all | bool | False | When True, extracts all pages. When False, extracts only the first page |
| max_workers | int | None | Maximum number of concurrent processes. Defaults to CPU count if None |

## Return Value

Both the function and class method return a list of strings containing the paths to all successfully extracted image files.

## Error Handling

The utility includes comprehensive error handling:
- Validates PDF existence
- Creates output directory if it doesn't exist
- Logs errors for individual page extraction failures
- Returns only successfully extracted page paths

## Performance Considerations

- The `max_workers` parameter can be adjusted based on your system's capabilities
- For very large PDFs, consider extracting in batches or limiting the worker count
- The `scale` parameter affects both image quality and memory usage

## Example

```python
# Example usage
pdf_path = "documents/sample.pdf"
    
# Extract only first page
first_page_images = extract_pdf_pages(pdf_path)
    
# Extract all pages with custom worker count
all_page_images = extract_pdf_pages(pdf_path, extract_all=True, max_workers=4)
```

## License

[MIT License](LICENSE)

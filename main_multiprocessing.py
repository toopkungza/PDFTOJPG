import os
import logging
from typing import Union, List
import pypdfium2 as pdfium2
from PIL import Image
import multiprocessing
from functools import partial

class PDFExtractor:
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize PDF extractor with configurable logging.
        
        Args:
            log_level: Logging level (default: INFO)
        """
        logging.basicConfig(
            level=log_level, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _extract_single_page(
        self, 
        pdf_path: str, 
        output_dir: str, 
        base_filename: str, 
        page_num: int, 
        scale: int = 4
    ) -> str:
        """
        Extract a single page from a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images
            base_filename: Base name for output files
            page_num: Page number to extract
            scale: Rendering scale
        
        Returns:
            Path to the extracted image file
        """
        try:
            # Open PDF document
            pdfobj = pdfium2.PdfDocument(pdf_path)
            
            # Render page
            page = pdfobj[page_num]
            pil_img = page.render(scale=scale).to_pil()
            
            # Generate output filename
            output_filename = os.path.join(
                output_dir, 
                f"{base_filename}_page{page_num+1}.jpg"
            )

            # Save image
            pil_img.save(output_filename, quality=95)
            
            # Close resources
            page.close()
            pdfobj.close()
            
            self.logger.info(f"Extracted page {page_num+1} to {output_filename}")
            
            return output_filename

        except Exception as page_error:
            self.logger.error(f"Error extracting page {page_num+1}: {page_error}")
            return None

    def extract_pdf_pages(
        self, 
        pdf_path: str, 
        output_dir: str = None, 
        scale: int = 4, 
        extract_all: bool = False,
        max_workers: int = None
    ) -> List[str]:
        """
        Extract pages from a PDF file using multiprocessing.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images (default: same as PDF)
            scale: Rendering scale (default: 4)
            extract_all: Extract all pages or just the first page (default: False)
            max_workers: Maximum number of concurrent processes (default: None = CPU count)
        
        Returns:
            List of paths to extracted image files
        """
        # Validate input
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Determine output directory
        if output_dir is None:
            output_dir = os.path.dirname(pdf_path) or '.'
        os.makedirs(output_dir, exist_ok=True)

        # Output filename base
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

        # Open PDF document to get total pages
        pdfobj = pdfium2.PdfDocument(pdf_path)
        total_pages = len(pdfobj)
        pdfobj.close()

        pages_to_extract = range(total_pages) if extract_all else [0]

        self.logger.info(f"Extracting from PDF: {pdf_path}")
        self.logger.info(f"Total pages: {total_pages}")

        # Determine number of workers
        if max_workers is None:
            max_workers = min(32, max(1, multiprocessing.cpu_count()))

        # Prepare partial function for multiprocessing
        extract_func = partial(
            self._extract_single_page, 
            pdf_path, 
            output_dir, 
            base_filename, 
            scale=scale
        )

        # Use multiprocessing to extract pages
        with multiprocessing.Pool(processes=max_workers) as pool:
            extracted_images = pool.map(extract_func, pages_to_extract)

        # Remove any None values (failed extractions)
        extracted_images = [img for img in extracted_images if img is not None]

        if not extracted_images:
            self.logger.warning("No images were extracted")

        return extracted_images

def extract_pdf_pages(
    pdf_path: str, 
    output_dir: str = None, 
    scale: int = 4, 
    extract_all: bool = False,
    max_workers: int = None
) -> List[str]:
    """
    Convenience function for extracting PDF pages using multiprocessing.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images
        scale: Rendering scale
        extract_all: Extract all pages or just the first page
        max_workers: Maximum number of concurrent processes
    
    Returns:
        List of extracted image paths
    """
    extractor = PDFExtractor()
    return extractor.extract_pdf_pages(
        pdf_path, 
        output_dir, 
        scale, 
        extract_all,
        max_workers
    )

# Example usage
if __name__ == '__main__':
    pdf_path = r"D:\Sukrit\Source_Codes\PDF\PDFTOJPG\1.pdf"
    
    # Extract only first page
    first_page_images = extract_pdf_pages(pdf_path)
    
    # Extract all pages with custom worker count
    all_page_images = extract_pdf_pages(pdf_path, extract_all=True, max_workers=4)
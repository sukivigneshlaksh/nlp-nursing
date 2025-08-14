"""
Medical PDF Ingestion Module
Handles extraction of text content from medical PDFs for downstream processing.
Part of Suki AI internship demonstration - basic document ingestion.
"""

import PyPDF2
import fitz  # PyMuPDF
from typing import List, Dict, Optional, Tuple
import logging
import os
from pathlib import Path
import time

# Configure logging for verbose output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MedicalPDFIngester:
    """
    A verbose and naive PDF ingestion class specifically designed for medical documents.
    Demonstrates basic PDF text extraction capabilities with multiple fallback methods.
    """
    
    def __init__(self, verbose_mode: bool = True):
        """
        Initialize the PDF ingester with configuration options.
        
        Args:
            verbose_mode (bool): Enable detailed logging and progress updates
        """
        self.verbose_mode = verbose_mode
        self.supported_extensions = ['.pdf']
        self.extraction_stats = {
            'total_files_processed': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'total_pages_processed': 0,
            'total_characters_extracted': 0
        }
        
        if self.verbose_mode:
            logger.info("Initializing MedicalPDFIngester...")
            logger.info(f"Supported file extensions: {self.supported_extensions}")
    
    def validate_pdf_file(self, file_path: str) -> bool:
        """
        Perform comprehensive validation of PDF file before processing.
        
        Args:
            file_path (str): Path to the PDF file to validate
            
        Returns:
            bool: True if file is valid and processable, False otherwise
        """
        if self.verbose_mode:
            logger.info(f"Starting validation for file: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            if self.verbose_mode:
                logger.error(f"File does not exist: {file_path}")
            return False
        
        # Check file extension
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in self.supported_extensions:
            if self.verbose_mode:
                logger.error(f"Unsupported file extension: {file_extension}")
            return False
        
        # Check file size (basic sanity check)
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            if self.verbose_mode:
                logger.error(f"File is empty: {file_path}")
            return False
        
        if self.verbose_mode:
            logger.info(f"File validation successful. Size: {file_size} bytes")
        
        return True
    
    def extract_text_with_pypdf2(self, file_path: str) -> Tuple[str, Dict]:
        """
        Extract text from PDF using PyPDF2 library.
        This is the primary extraction method with basic functionality.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            Tuple[str, Dict]: Extracted text and metadata
        """
        if self.verbose_mode:
            logger.info(f"Attempting text extraction with PyPDF2 for: {file_path}")
        
        extracted_text = ""
        metadata = {
            'extraction_method': 'PyPDF2',
            'pages_processed': 0,
            'extraction_time': 0,
            'success': False
        }
        
        start_time = time.time()
        
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                total_pages = len(pdf_reader.pages)
                
                if self.verbose_mode:
                    logger.info(f"PDF contains {total_pages} pages")
                
                for page_number, page in enumerate(pdf_reader.pages):
                    if self.verbose_mode:
                        logger.info(f"Processing page {page_number + 1}/{total_pages}")
                    
                    page_text = page.extract_text()
                    extracted_text += f"\n--- PAGE {page_number + 1} ---\n"
                    extracted_text += page_text
                    extracted_text += f"\n--- END PAGE {page_number + 1} ---\n"
                    
                    metadata['pages_processed'] += 1
                
                metadata['extraction_time'] = time.time() - start_time
                metadata['success'] = True
                
                if self.verbose_mode:
                    logger.info(f"PyPDF2 extraction completed successfully in {metadata['extraction_time']:.2f} seconds")
        
        except Exception as extraction_error:
            if self.verbose_mode:
                logger.error(f"PyPDF2 extraction failed: {str(extraction_error)}")
            metadata['error'] = str(extraction_error)
        
        return extracted_text, metadata
    
    def extract_text_with_pymupdf(self, file_path: str) -> Tuple[str, Dict]:
        """
        Extract text from PDF using PyMuPDF (fitz) library as fallback method.
        Often more robust than PyPDF2 for complex medical documents.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            Tuple[str, Dict]: Extracted text and metadata
        """
        if self.verbose_mode:
            logger.info(f"Attempting text extraction with PyMuPDF for: {file_path}")
        
        extracted_text = ""
        metadata = {
            'extraction_method': 'PyMuPDF',
            'pages_processed': 0,
            'extraction_time': 0,
            'success': False
        }
        
        start_time = time.time()
        
        try:
            pdf_document = fitz.open(file_path)
            total_pages = pdf_document.page_count
            
            if self.verbose_mode:
                logger.info(f"PDF contains {total_pages} pages")
            
            for page_number in range(total_pages):
                if self.verbose_mode:
                    logger.info(f"Processing page {page_number + 1}/{total_pages}")
                
                page = pdf_document[page_number]
                page_text = page.get_text()
                
                extracted_text += f"\n--- PAGE {page_number + 1} ---\n"
                extracted_text += page_text
                extracted_text += f"\n--- END PAGE {page_number + 1} ---\n"
                
                metadata['pages_processed'] += 1
            
            pdf_document.close()
            
            metadata['extraction_time'] = time.time() - start_time
            metadata['success'] = True
            
            if self.verbose_mode:
                logger.info(f"PyMuPDF extraction completed successfully in {metadata['extraction_time']:.2f} seconds")
        
        except Exception as extraction_error:
            if self.verbose_mode:
                logger.error(f"PyMuPDF extraction failed: {str(extraction_error)}")
            metadata['error'] = str(extraction_error)
        
        return extracted_text, metadata
    
    def process_single_pdf(self, file_path: str) -> Dict:
        """
        Process a single PDF file with comprehensive error handling and fallback methods.
        
        Args:
            file_path (str): Path to the PDF file to process
            
        Returns:
            Dict: Processing results including extracted text and metadata
        """
        if self.verbose_mode:
            logger.info(f"Starting processing of PDF file: {file_path}")
        
        processing_result = {
            'file_path': file_path,
            'extracted_text': "",
            'character_count': 0,
            'processing_successful': False,
            'extraction_metadata': {},
            'processing_time': 0
        }
        
        start_time = time.time()
        
        # Validate file before processing
        if not self.validate_pdf_file(file_path):
            processing_result['error'] = "File validation failed"
            return processing_result
        
        # Try primary extraction method (PyPDF2)
        extracted_text, metadata = self.extract_text_with_pypdf2(file_path)
        
        # If primary method fails, try fallback method (PyMuPDF)
        if not metadata['success'] or len(extracted_text.strip()) == 0:
            if self.verbose_mode:
                logger.warning("Primary extraction method failed or returned empty text, trying fallback method...")
            
            extracted_text, metadata = self.extract_text_with_pymupdf(file_path)
        
        # Update processing result
        processing_result['extracted_text'] = extracted_text
        processing_result['character_count'] = len(extracted_text)
        processing_result['processing_successful'] = metadata['success']
        processing_result['extraction_metadata'] = metadata
        processing_result['processing_time'] = time.time() - start_time
        
        # Update global statistics
        self.extraction_stats['total_files_processed'] += 1
        if metadata['success']:
            self.extraction_stats['successful_extractions'] += 1
            self.extraction_stats['total_pages_processed'] += metadata.get('pages_processed', 0)
            self.extraction_stats['total_characters_extracted'] += len(extracted_text)
        else:
            self.extraction_stats['failed_extractions'] += 1
        
        if self.verbose_mode:
            logger.info(f"PDF processing completed in {processing_result['processing_time']:.2f} seconds")
            logger.info(f"Extracted {processing_result['character_count']} characters")
        
        return processing_result
    
    def process_multiple_pdfs(self, file_paths: List[str]) -> List[Dict]:
        """
        Process multiple PDF files sequentially (non-concurrent version).
        This demonstrates the basic approach before introducing concurrency.
        
        Args:
            file_paths (List[str]): List of PDF file paths to process
            
        Returns:
            List[Dict]: List of processing results for each file
        """
        if self.verbose_mode:
            logger.info(f"Starting sequential processing of {len(file_paths)} PDF files")
        
        all_results = []
        total_start_time = time.time()
        
        for file_index, file_path in enumerate(file_paths):
            if self.verbose_mode:
                logger.info(f"Processing file {file_index + 1}/{len(file_paths)}: {file_path}")
            
            file_result = self.process_single_pdf(file_path)
            all_results.append(file_result)
        
        total_processing_time = time.time() - total_start_time
        
        if self.verbose_mode:
            logger.info(f"Sequential processing completed in {total_processing_time:.2f} seconds")
            logger.info(f"Successfully processed {self.extraction_stats['successful_extractions']} files")
            logger.info(f"Failed to process {self.extraction_stats['failed_extractions']} files")
        
        return all_results
    
    def get_extraction_statistics(self) -> Dict:
        """
        Get comprehensive statistics about the extraction process.
        
        Returns:
            Dict: Detailed extraction statistics
        """
        return self.extraction_stats.copy()


def demonstrate_basic_pdf_ingestion():
    """
    Demonstration function showing basic PDF ingestion capabilities.
    This represents the first stage of the Suki AI internship progression.
    """
    print("=" * 60)
    print("BASIC PDF INGESTION DEMONSTRATION")
    print("Stage 1: Simple document text extraction")
    print("=" * 60)
    
    # Initialize the ingester with verbose mode
    ingester = MedicalPDFIngester(verbose_mode=True)
    
    # Example usage with sample files (would need actual PDF files)
    sample_files = [
        "/Users/valaksh/Desktop/suki/nlp-nursing/data/pdf/CMS_Form.pdf"
    ]
    
    print(f"\nProcessing {len(sample_files)} sample medical PDF(s)...")
    
    results = ingester.process_multiple_pdfs(sample_files)
    
    print(f"\nExtraction Statistics:")
    stats = ingester.get_extraction_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return results


if __name__ == "__main__":
    # Run the basic demonstration
    results = demonstrate_basic_pdf_ingestion()
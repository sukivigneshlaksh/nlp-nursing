"""
Concurrent Medical Document Processing
Shows GPU-inspired concurrency for processing multiple documents.
"""

import asyncio
import time
from typing import List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pdf_ingestion import MedicalPDFIngester
from agentic_extraction import MedicalExtractionAgent


class ConcurrentMedicalProcessor:
    """Processes multiple medical documents concurrently."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.ingester = MedicalPDFIngester(verbose_mode=False)
        self.agent = MedicalExtractionAgent()
    
    def process_single_document(self, file_path: str):
        """Process one document (for threading)."""
        print(f"Processing {file_path}...")
        
        # Extract text
        result = self.ingester.process_single_pdf(file_path)
        if not result['processing_successful']:
            return {'error': 'PDF extraction failed', 'file': file_path}
        
        # Extract medical data
        doc = self.agent.execute_plan(result['extracted_text'])
        doc.document_id = file_path
        
        return {'success': True, 'document': doc, 'file': file_path}
    
    def process_sequential(self, file_paths: List[str]):
        """Process documents one by one (slow way)."""
        print("Sequential processing (like single-threaded CPU)...")
        start = time.time()
        
        results = []
        for path in file_paths:
            result = self.process_single_document(path)
            results.append(result)
        
        duration = time.time() - start
        print(f"Sequential: {duration:.2f} seconds")
        return results, duration
    
    def process_concurrent_threads(self, file_paths: List[str]):
        """Process documents concurrently with threads (like GPU cores)."""
        print("Concurrent processing with threads (like GPU parallelism)...")
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self.process_single_document, file_paths))
        
        duration = time.time() - start
        print(f"Concurrent threads: {duration:.2f} seconds")
        return results, duration
    
    def process_concurrent_processes(self, file_paths: List[str]):
        """Process documents with multiprocessing (like multiple GPUs)."""
        print("Concurrent processing with processes (like multiple GPUs)...")
        start = time.time()
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self.process_single_document, file_paths))
        
        duration = time.time() - start
        print(f"Concurrent processes: {duration:.2f} seconds")
        return results, duration


class SingleAPIProcessor:
    """Shows how tasks become simple enough for single API call."""
    
    def process_all_at_once(self, file_paths: List[str]):
        """Process everything in one API call (future evolution)."""
        print("Single API call processing (future: everything in one request)...")
        start = time.time()
        
        # Simulate powerful API that processes everything at once
        time.sleep(0.5)  # Simulate API call
        
        results = []
        for path in file_paths:
            results.append({
                'success': True,
                'file': path,
                'note': 'Processed by advanced single API call'
            })
        
        duration = time.time() - start
        print(f"Single API: {duration:.2f} seconds")
        return results, duration


def demonstrate_concurrency_progression():
    """Show the progression from sequential to concurrent to single API."""
    print("=" * 60)
    print("CONCURRENCY PROGRESSION DEMONSTRATION")
    print("Core idea: GPU-inspired concurrency → eventual API simplification")
    print("=" * 60)
    
    # Simulate multiple PDF files
    sample_files = [
        "/Users/valaksh/Desktop/suki/nlp-nursing/data/pdf/CMS_Form.pdf",
        "/Users/valaksh/Desktop/suki/nlp-nursing/data/pdf/CMS_Form.pdf",  # Same file for demo
        "/Users/valaksh/Desktop/suki/nlp-nursing/data/pdf/CMS_Form.pdf"
    ]
    
    processor = ConcurrentMedicalProcessor(max_workers=2)
    single_api = SingleAPIProcessor()
    
    print(f"\nProcessing {len(sample_files)} documents...")
    
    # Sequential processing
    seq_results, seq_time = processor.process_sequential(sample_files)
    
    # Concurrent processing  
    conc_results, conc_time = processor.process_concurrent_threads(sample_files)
    
    # Single API processing
    api_results, api_time = single_api.process_all_at_once(sample_files)
    
    print(f"\n" + "="*40)
    print("RESULTS SUMMARY:")
    print(f"Sequential time: {seq_time:.2f}s")
    print(f"Concurrent time: {conc_time:.2f}s") 
    print(f"Single API time: {api_time:.2f}s")
    
    if seq_time > 0:
        speedup = seq_time / conc_time
        print(f"Speedup from concurrency: {speedup:.1f}x")
    
    print(f"\nProgression insight:")
    print(f"1. Basic processing: slow, sequential")
    print(f"2. GPU-inspired concurrency: faster, parallel")
    print(f"3. Advanced APIs: eventually simple enough for single call")


if __name__ == "__main__":
    demonstrate_concurrency_progression()
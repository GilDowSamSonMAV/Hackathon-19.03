"""
HaMoach — Document Sanitizer
==============================
Strips prompt injection patterns from document content DURING ingestion.
This is Layer 1 of the security defense (input validation).

Defense-in-depth approach:
  Layer 1: Sanitize documents on ingest (this module)
  Layer 2: Guard agent classifies user input (guard.py)
  Layer 3: System/data separation via XML tags in prompts
  Layer 4: Confidence threshold refuses low-relevance answers
"""

import re
from agents.prompts import INJECTION_PATTERNS, REDACTION_REPLACEMENT


def sanitize_text(text: str) -> tuple[str, list[str]]:
    """
    Remove prompt injection patterns from document text.
    
    Returns:
        (sanitized_text, list of detected patterns)
    """
    detections = []
    sanitized = text
    
    for pattern in INJECTION_PATTERNS:
        matches = re.findall(pattern, sanitized)
        if matches:
            detections.extend(matches)
            sanitized = re.sub(pattern, REDACTION_REPLACEMENT, sanitized)
    
    return sanitized, detections


def sanitize_chunk(chunk: str) -> str:
    """
    Quick sanitize for a single chunk. Returns cleaned text.
    Use this in the chunking pipeline.
    """
    sanitized, _ = sanitize_text(chunk)
    return sanitized


# --- Ingestion-time report ---
def sanitize_document(filename: str, content: str) -> tuple[str, dict]:
    """
    Sanitize an entire document and return a report.
    
    Returns:
        (sanitized_content, report_dict)
    """
    sanitized, detections = sanitize_text(content)
    
    report = {
        "filename": filename,
        "original_length": len(content),
        "sanitized_length": len(sanitized),
        "injections_found": len(detections),
        "injection_details": detections[:10],  # cap at 10 for display
        "was_modified": len(detections) > 0,
    }
    
    if detections:
        print(f"  ⚠️  {filename}: Removed {len(detections)} injection pattern(s)")
        for d in detections[:3]:
            print(f"      → {d[:80]}...")
    
    return sanitized, report

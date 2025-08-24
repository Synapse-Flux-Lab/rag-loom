import re
from typing import List
from loguru import logger

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if chunk_overlap >= chunk_size:
            raise ValueError("Chunk overlap must be smaller than chunk size")
    
    def sliding_window_chunk(self, text: str) -> List[str]:
        """Split text into overlapping chunks using sliding window approach"""
        if not text.strip():
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate end position for this chunk
            end = start + self.chunk_size
            
            # If we're at the end, take the remaining text
            if end >= text_length:
                chunk = text[start:]
                chunks.append(chunk)
                break
            
            # Try to find a good breaking point (sentence end or paragraph)
            break_point = self._find_break_point(text, start, end)
            
            if break_point > start:  # Found a good break point
                chunk = text[start:break_point].strip()
                chunks.append(chunk)
                start = break_point - self.chunk_overlap
            else:
                # No good break point found, break at chunk size
                chunk = text[start:end].strip()
                chunks.append(chunk)
                start = end - self.chunk_overlap
            
            # Ensure we don't go backwards
            start = max(start, 0)
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def _find_break_point(self, text: str, start: int, end: int) -> int:
        """Find a natural break point in the text"""
        # Look for sentence endings first
        sentence_endings = ['.', '!', '?', '\n\n']
        
        for pos in range(end, start, -1):
            if pos < len(text) and text[pos] in sentence_endings:
                # Check if it's actually the end of a sentence
                if self._is_sentence_end(text, pos):
                    return pos + 1
        
        # Look for paragraph breaks or other natural breaks
        for pos in range(end, start, -1):
            if pos < len(text) and text[pos] == '\n':
                return pos + 1
        
        # Look for space breaks
        for pos in range(end, start, -1):
            if pos < len(text) and text[pos].isspace():
                return pos + 1
        
        return end  # No good break point found
    
    def _is_sentence_end(self, text: str, pos: int) -> bool:
        """Check if position is actually the end of a sentence"""
        if pos >= len(text) - 1:
            return True
        
        # Check if next character is whitespace and following character is uppercase
        if (text[pos] in ['.', '!', '?'] and 
            (pos + 1 >= len(text) or text[pos + 1].isspace()) and
            (pos + 2 < len(text) and text[pos + 2].isupper())):
            return True
        
        return False

    def chunk_by_sentences(self, text: str) -> List[str]:
        """Alternative chunking method: split by sentences and group into chunks"""
        # Simple sentence splitting (for demonstration)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_length = len(sentence)
            
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Current chunk is full, save it
                chunks.append(' '.join(current_chunk))
                # Start new chunk with overlap
                overlap_start = max(0, len(current_chunk) - 
                                  self.chunk_overlap // (current_length // max(1, len(current_chunk))))
                current_chunk = current_chunk[overlap_start:]
                current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1
            
            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for space
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
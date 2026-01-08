"""
Módulo para procesar PDFs y extraer texto para RAG
"""
import fitz  # PyMuPDF
from typing import List, Dict
import tempfile
import os
import httpx


class PDFProcessor:
    """Procesa PDFs y divide el contenido en chunks para RAG"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    async def download_pdf(self, url: str) -> str:
        """Descarga PDF desde URL y guarda temporalmente"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            # Guardar en archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(response.content)
                return tmp_file.name
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrae texto completo de un PDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += f"\n--- Página {page_num + 1} ---\n"
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Error al extraer texto del PDF: {str(e)}")
    
    def split_into_chunks(self, text: str) -> List[Dict[str, str]]:
        """Divide el texto en chunks con overlap"""
        chunks = []
        text_length = len(text)
        
        start = 0
        chunk_id = 0
        
        while start < text_length:
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                "id": f"chunk_{chunk_id}",
                "text": chunk_text.strip(),
                "start": start,
                "end": min(end, text_length)
            })
            
            start += self.chunk_size - self.chunk_overlap
            chunk_id += 1
        
        return chunks
    
    async def process_pdf(self, pdf_source: str) -> Dict:
        """Procesa PDF completo: descarga, extrae texto y crea chunks"""
        # Determinar si es URL o archivo local
        if pdf_source.startswith('http://') or pdf_source.startswith('https://'):
            pdf_path = await self.download_pdf(pdf_source)
            is_temp = True
        else:
            pdf_path = pdf_source
            is_temp = False
        
        try:
            # Extraer texto
            text = self.extract_text_from_pdf(pdf_path)
            
            # Dividir en chunks
            chunks = self.split_into_chunks(text)
            
            return {
                "success": True,
                "full_text": text,
                "chunks": chunks,
                "num_chunks": len(chunks),
                "text_length": len(text)
            }
        finally:
            # Limpiar archivo temporal si se descargó
            if is_temp and os.path.exists(pdf_path):
                os.unlink(pdf_path)

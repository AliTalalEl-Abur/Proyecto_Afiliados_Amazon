"""
Agente LangChain para generar artículos técnicos usando RAG
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import Dict, List
import os


class ArticleGenerator:
    """Genera artículos técnicos usando RAG con LangChain"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        self.llm = ChatOpenAI(
            temperature=0.3,
            model=model,
            api_key=api_key
        )
        
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        
        # Template para el prompt
        self.prompt_template = """Actúa como un técnico experto en domótica y productos electrónicos.

Contexto del manual técnico:
{context}

Error reportado: {error}
Modelo del producto: {model}

Tu tarea es crear un artículo técnico completo que incluya:

1. **Título**: Un título claro y descriptivo (máximo 80 caracteres)
2. **Introducción**: Breve explicación del error y su impacto
3. **Significado del error**: Qué significa técnicamente este error
4. **Diagnóstico**: Cómo identificar la causa del problema
5. **Solución paso a paso**: Instrucciones claras y numeradas para resolver el error
6. **Fallos comunes**: Otros problemas relacionados que suelen ocurrir
7. **Productos recomendados**: Lista de 2-3 productos que pueden ayudar a resolver el problema (herramientas, repuestos, etc.)

IMPORTANTE: 
- Sé específico y técnico pero comprensible
- Usa información del manual técnico proporcionado
- Para los productos, menciona nombre genérico y tipo (ej: "Multímetro digital", "Cable HDMI 2.1", "Kit de herramientas")
- NO inventes información que no esté en el contexto

Responde SOLO en formato JSON con esta estructura:
{{
  "title": "título del artículo",
  "introduction": "introducción",
  "error_meaning": "significado del error",
  "diagnosis": "cómo diagnosticar",
  "solution_steps": ["paso 1", "paso 2", "paso 3"],
  "common_failures": ["fallo 1", "fallo 2"],
  "recommended_products": [
    {{"name": "nombre producto 1", "type": "tipo", "reason": "por qué es útil"}},
    {{"name": "nombre producto 2", "type": "tipo", "reason": "por qué es útil"}}
  ]
}}

Pregunta: {question}
"""
    
    def create_vectorstore(self, chunks: List[Dict]) -> FAISS:
        """Crea vectorstore FAISS desde chunks de texto"""
        texts = [chunk["text"] for chunk in chunks]
        
        # Crear vectorstore
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings
        )
        
        return vectorstore
    
    async def generate_article(
        self,
        chunks: List[Dict],
        error: str,
        model: str
    ) -> Dict:
        """Genera artículo técnico usando RAG"""
        
        # Crear vectorstore
        vectorstore = self.create_vectorstore(chunks)
        
        # Crear prompt
        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "error", "model", "question"]
        )
        
        # Crear chain de QA
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        # Generar respuesta
        question = f"Genera un artículo técnico completo sobre cómo solucionar el error '{error}' en el modelo '{model}'."
        
        result = qa_chain.invoke({
            "query": question,
            "error": error,
            "model": model
        })
        
        return {
            "success": True,
            "result": result["result"],
            "source_documents": [doc.page_content[:200] for doc in result["source_documents"]]
        }
    
    def parse_llm_response(self, llm_response: str) -> Dict:
        """Parsea la respuesta del LLM en formato JSON"""
        import json
        import re
        
        # Intentar extraer JSON de la respuesta
        try:
            # Buscar contenido JSON entre llaves
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Si no hay JSON, devolver estructura básica
                return {
                    "title": "Error en el formato de respuesta",
                    "content": llm_response,
                    "error": "No se pudo parsear la respuesta como JSON"
                }
        except json.JSONDecodeError as e:
            return {
                "title": "Error al parsear respuesta",
                "content": llm_response,
                "error": f"Error de JSON: {str(e)}"
            }

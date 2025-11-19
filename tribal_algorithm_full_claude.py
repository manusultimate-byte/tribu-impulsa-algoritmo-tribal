# TRIBU IMPULSA - ALGORITMO TRIBAL - SEGURO

import os
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import AzureOpenAI

@dataclass
class Emprendedor:
    id: str
    nombre: str
    email: str
    empresa: str
    area_trabajo: str
    sub_area: str
    industria: str
    tamano_empresa: str
    fase_negocio: str
    necesidades: List[str]
    ofertas: List[str]
    descripcion: str
    embedding: List[float] = None

@dataclass
class Match:
    emprendedor_id: str
    matched_con_id: str
    matched_nombre: str
    matched_empresa: str
    score_afinidad: float
    razones: List[str]
    categoria: str

class TribalAlgorithm:
    def __init__(self):
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.openai = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
        self.collection_name = "tribu_impulsa"
        self._init_collection()
    
    def _init_collection(self):
        """Crear colección si no existe"""
        collections = [c.name for c in self.qdrant.get_collections().collections]
        if self.collection_name not in collections:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
    
    def generar_embedding(self, emprendedor: Emprendedor) -> List[float]:
        texto = f"""
{emprendedor.nombre} - {emprendedor.empresa}
Área: {emprendedor.area_trabajo} / {emprendedor.sub_area}
Industria: {emprendedor.industria}
Tamaño: {emprendedor.tamano_empresa}
Fase: {emprendedor.fase_negocio}
Necesidades: {', '.join(emprendedor.necesidades)}
Ofertas: {', '.join(emprendedor.ofertas)}
{emprendedor.descripcion}
        """
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=texto
        )
        return response.data[0].embedding
    
    def guardar_en_qdrant(self, emprendedor: Emprendedor):
        if not emprendedor.embedding:
            emprendedor.embedding = self.generar_embedding(emprendedor)
        point = PointStruct(
            id=emprendedor.id,
            vector=emprendedor.embedding,
            payload={
                "nombre": emprendedor.nombre,
                "email": emprendedor.email,
                "empresa": emprendedor.empresa,
                "area_trabajo": emprendedor.area_trabajo,
                "sub_area": emprendedor.sub_area,
                "necesidades": emprendedor.necesidades,
                "ofertas": emprendedor.ofertas
            }
        )
        self.qdrant.upsert(collection_name=self.collection_name, points=[point])
        print(f"✅ {emprendedor.nombre} guardado")
    
    def buscar_matches(self, emprendedor: Emprendedor, limit: int = 10) -> List[Match]:
        if not emprendedor.embedding:
            emprendedor.embedding = self.generar_embedding(emprendedor)
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=emprendedor.embedding,
            limit=limit + 1
        )
        matches = []
        for result in results:
            if result.id != emprendedor.id:
                score = self._calcular_score(emprendedor, result.payload, result.score)
                razones = self._generar_razones(emprendedor, result.payload)
                match = Match(
                    emprendedor_id=emprendedor.id,
                    matched_con_id=result.id,
                    matched_nombre=result.payload['nombre'],
                    matched_empresa=result.payload['empresa'],
                    score_afinidad=score,
                    razones=razones,
                    categoria=self._categorizar(score)
                )
                matches.append(match)
        return sorted(matches, key=lambda m: m.score_afinidad, reverse=True)[:limit]
    
    def _calcular_score(self, emp1: Emprendedor, emp2_payload: Dict, similitud: float) -> float:
        score = similitud * 0.4
        if emp1.area_trabajo == emp2_payload.get('area_trabajo'):
            score += 0.1
        if emp1.sub_area == emp2_payload.get('sub_area'):
            score += 0.1
        necesidades_emp1 = set([n.lower() for n in emp1.necesidades])
        ofertas_emp2 = set([o.lower() for o in emp2_payload.get('ofertas', [])])
        complementariedad = len(necesidades_emp1 & ofertas_emp2) / max(len(necesidades_emp1), 1)
        score += complementariedad * 0.3
        if emp1.tamano_empresa == emp2_payload.get('tamano_empresa'):
            score += 0.1
        else:
            score += 0.05
        return min(score, 1.0)
    
    def _generar_razones(self, emp1: Emprendedor, emp2_payload: Dict) -> List[str]:
        prompt = f"""
Explica en 3 razones breves (max 12 palabras cada una) por qué estos emprendedores deberían conectarse:

1: {emp1.nombre} - {emp1.area_trabajo} - Necesita: {', '.join(emp1.necesidades)}
2: {emp2_payload['nombre']} - {emp2_payload['area_trabajo']} - Ofrece: {', '.join(emp2_payload['ofertas'])}

Formato: Una razón por línea, sin numeración.
        """
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            razones = response.choices[0].message.content.strip().split('\n')[:3]
            return [r.strip() for r in razones if r.strip()]
        except:
            return ["Perfiles complementarios", "Potencial colaboración", "Sinergia estratégica"]
    
    def _categorizar(self, score: float) -> str:
        if score >= 0.75:
            return "alta"
        elif score >= 0.55:
            return "media"
        return "baja"

def main():
    algorithm = TribalAlgorithm()
    emprendedores = [
        Emprendedor(
            id="emp_001",
            nombre="Juan Pérez",
            email="juan@tech.cl",
            empresa="TechStartup",
            area_trabajo="Tecnología",
            sub_area="Desarrollo Software",
            industria="B2B",
            tamano_empresa="Pequeña",
            fase_negocio="Crecimiento",
            necesidades=["Financiamiento", "Networking"],
            ofertas=["Desarrollo Web", "Consultoría"],
            descripcion="Desarrollamos soluciones web para empresas"
        ),
        # ... agrega más emprendedores aquí / o lee desde Google Sheets
    ]
    for emp in emprendedores:
        algorithm.guardar_en_qdrant(emp)
    for emp in emprendedores:
        matches = algorithm.buscar_matches(emp, limit=10)
        print(f"\n🎯 Matches para {emp.nombre}:")
        for m in matches[:3]:
            print(f"  - {m.matched_nombre} ({m.score_afinidad:.2f}) - {m.categoria}")
            print(f"    Razones: {m.razones}")

if __name__ == "__main__":
    main()

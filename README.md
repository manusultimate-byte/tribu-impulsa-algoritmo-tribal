# 🚀 Tribu Impulsa - Algoritmo Tribal

Sistema de matching inteligente para emprendedores chilenos usando **Claude Sonnet 4** + **Qdrant Vector Database**.

## 💡 ¿Qué hace?

El **Algoritmo Tribal** conecta emprendedores basándose en:
- ✅ Similitud de perfiles usando embeddings de IA
- ✅ Complementariedad de necesidades y ofertas
- ✅ Compatibilidad de área de negocio
- ✅ Fase de crecimiento y tamaño de empresa

## 🎯 Características

- **Embeddings de Alta Calidad**: Claude Sonnet 4 analiza perfiles completos
- **Vector Search**: Qdrant para búsquedas ultrarrápidas
- **Razones Inteligentes**: Claude genera explicaciones contextuales
- **Categorización**: Matches de alta, media y baja afinidad
- **Exportación JSON**: Resultados listos para integración

## 💰 Costos con Azure AI Foundry

Con **$15,000 USD** en créditos:

| Escenario | Costo/mes | Duración |
|-----------|-----------|----------|
| 100 usuarios | $1.33 | 936 años 🤯 |
| 500 usuarios | $6.67 | 187 años |
| 1000 usuarios | $13.35 | **93 años** |
| 5000 usuarios | $66.75 | 18 años |

## 📦 Instalación

```bash
pip install qdrant-client anthropic numpy
```

## ⚙️ Configuración

El código ya incluye las credenciales configuradas:
- ✅ Qdrant Cloud (conexión activa)
- ✅ Azure Anthropic Claude (Sonnet 4 + Haiku 4)

## 🚀 Uso

```python
from tribal_algorithm_full_claude import TribalAlgorithmFullClaude, Emprendedor

# Inicializar
algorithm = TribalAlgorithmFullClaude()

# Crear perfil
emprendedor = Emprendedor(
    id="emp_001",
    nombre="María González",
    email="maria@startup.cl",
    empresa="TechStartup",
    area_trabajo="Tecnología",
    sub_area="Desarrollo Software",
    industria="B2B",
    tamano_empresa="Pequeña",
    fase_negocio="Crecimiento",
    necesidades=["Financiamiento", "Marketing"],
    ofertas=["Desarrollo Web", "Consultoría"],
    descripcion="Desarrollamos soluciones SaaS"
)

# Guardar en Qdrant
algorithm.guardar_emprendedor(emprendedor)

# Generar matches
matches = algorithm.generar_matches(emprendedor, top_n=10)

# Ver resultados
for match in matches:
    print(f"{match.matched_nombre} - Score: {match.score_afinidad:.2f}")
    print(f"Razones: {match.razones}")
```

## 🧪 Ejecutar Test

```bash
python tribal_algorithm_full_claude.py
```

El test incluye 4 emprendedores de ejemplo y genera matches automáticamente.

## 📊 Output

El script genera un archivo `tribu_impulsa_matches.json` con todos los matches:

```json
[
  {
    "emprendedor_id": "emp_001",
    "matched_con_id": "emp_002",
    "matched_nombre": "Juan Pérez",
    "matched_empresa": "InnovaCorp",
    "score_afinidad": 0.85,
    "categoria": "alta",
    "razones": [
      "Sinergia tecnológica para escalamiento conjunto",
      "Complementan servicios en ecosistema SaaS chileno",
      "Oportunidad de co-desarrollo con IA y web"
    ]
  }
]
```

## 🏗️ Arquitectura

```
Usuario → Claude Sonnet 4 (Embedding) → Qdrant (Vector Search) → Claude (Razones) → JSON
```

1. **Análisis de Perfil**: Claude Sonnet 4 genera embedding de 1024 dimensiones
2. **Búsqueda Vectorial**: Qdrant encuentra emprendedores similares
3. **Scoring**: Algoritmo combina similitud + complementariedad
4. **Razones**: Claude genera explicaciones contextuales
5. **Output**: JSON con matches categorizados

## 🔧 Componentes

### Clase Principal: `TribalAlgorithmFullClaude`

**Métodos principales:**
- `guardar_emprendedor(emprendedor)` - Guarda perfil en Qdrant
- `generar_matches(emprendedor, top_n=10)` - Genera matches
- `exportar_matches_json(matches, filename)` - Exporta resultados

### Dataclasses

**`Emprendedor`**: Perfil completo del emprendedor
- Datos básicos (nombre, email, empresa)
- Caracterización (área, sub-área, industria)
- Necesidades y ofertas
- Metadata (fase, tamaño, descripción)

**`Match`**: Resultado de matching
- IDs de emprendedores
- Score de afinidad (0-1)
- Similitud de embedding
- 3 razones contextuales
- Categoría (alta/media/baja)

## 📈 Algoritmo de Scoring

```python
Score Total = 
  50% Similitud Embedding (Claude) +
  20% Match de Área/Sub-área +
  25% Complementariedad Necesidades-Ofertas +
  5% Compatibilidad Tamaño/Fase
```

## 🎯 Categorías de Match

- **Alta** (≥0.75): Sinergia excepcional
- **Media** (0.55-0.74): Buena compatibilidad
- **Baja** (0.50-0.54): Potencial interesante

## 🔐 Seguridad

Las credenciales están incluidas para el MVP. Para producción:
- Usar variables de entorno
- Rotar claves periódicamente
- Implementar rate limiting

## 📝 Próximos Pasos

- [ ] Integración con Google Sheets
- [ ] API REST para frontend
- [ ] Dashboard de visualización
- [ ] Notificaciones automáticas
- [ ] Analytics de matches exitosos

## 👥 Equipo

**Tribu Impulsa** - Dafna y Doraluz  
**Desarrollo**: EL REY DE LAS PÁGINAS  
**IA Stack**: Azure AI Foundry + Claude Sonnet 4 + Qdrant

## 📄 Licencia

Propiedad de Tribu Impulsa. Todos los derechos reservados.

---

**🚀 Powered by Claude Sonnet 4 & Qdrant**  
**💰 $15,000 USD = 93+ años de uso**

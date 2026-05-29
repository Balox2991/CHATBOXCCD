<div align="center">

<img src="https://img.shields.io/badge/UNAB-Centro%20de%20Competencias%20Digitales-1B2A4A?style=for-the-badge" />

# 🎓SOMNOS - Chatbot Inteligente CCD  — UNAB

### Asistente Digital del Centro de Competencias Digitales
**Universidad Autónoma de Bucaramanga**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![NVIDIA](https://img.shields.io/badge/NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com)
[![AWS](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)

---

> 💬 *"Un chatbot inteligente que responde preguntas sobre la ruta de competencias digitales, consulta tu progreso en tiempo real y te guía en tu camino hacia la insignia CCD."*

</div>

---

## 📋 Tabla de Contenidos

- [Resumen del Proyecto](#-resumen-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [Workflow en n8n](#-workflow-en-n8n)
- [Ruta de Competencias Digitales](#-ruta-de-competencias-digitales)
- [Interfaz Web Streamlit](#-interfaz-web---streamlit)
- [Base de Datos](#-base-de-datos)
- [Sistema RAG](#-sistema-rag)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [Ejemplos de Interacción](#-ejemplos-de-interacción)
- [Criterios de Evaluación](#-criterios-de-evaluación)
- [Equipo](#-equipo)

---

## 📌 Resumen del Proyecto

El **Chatbot CCD UNAB** es un asistente digital inteligente desarrollado como proyecto de **Ciencia de Datos** para la Universidad Autónoma de Bucaramanga. Permite a los estudiantes consultar en tiempo real información sobre la **Ruta de Competencias Digitales** del Centro de Competencias Digitales (CCD).

### ¿Qué puede hacer?

| Funcionalidad | Descripción |
|---|---|
| 📚 Consulta de cursos | Informa sobre los 3 pilares y cursos disponibles |
| 📊 Progreso académico | Consulta tu avance real en la BD institucional |
| 📅 Calendario CCD | Fechas de inscripciones, diagnóstica e inicio |
| 🏅 Insignia CCD | Requisitos y estado para obtenerla |
| 🧠 Memoria de conversación | Recuerda el contexto de la sesión |
| 🌐 Noticias y cursos nuevos | Detecta novedades del sitio CCD |
| 🔍 RAG SINTETICO | Consulta documentos oficiales del CCD |

---

## 🏗️ Arquitectura del Sistema

### Diagrama funcional

```
  ┌─────────────────────────────────────────────────┐
  │              Usuario (Streamlit)                 │
  └─────────────────────┬───────────────────────────┘
                        │ HTTP POST
                        ▼
  ┌─────────────────────────────────────────────────┐
  │           n8n Webhook (AWS EC2)                  │
  │         chatbot-grupobien [POST]                 │
  └─────────────────────┬───────────────────────────┘
                        │
                        ▼
  ┌─────────────────────────────────────────────────┐
  │         Execute a SQL query (Postgres)           │
  │    BD cosmos UNAB → progreso del estudiante      │
  └─────────────────────┬───────────────────────────┘
                        │
                        ▼
  ┌─────────────────────────────────────────────────┐
  │                  AI Agent                        │
  │         LLaMA 3.1 8B via NVIDIA NIM             │
  │                                                  │
  │  ┌──────────────┐  ┌──────────────────────────┐ │
  │  │ OpenAI Chat  │  │    Simple Memory          │ │
  │  │ Model(NVIDIA)│  │  (historial sesión)       │ │
  │  └──────────────┘  └──────────────────────────┘ │
  │                                                  │
  │  ┌──────────────┐  ┌──────────────────────────┐ │
  │  │ HTTP Request │  │    HTTP Request1          │ │
  │  │  Tool: RAG   │  │  Tool: Calendario         │ │
  │  └──────────────┘  └──────────────────────────┘ │
  └─────────────────────┬───────────────────────────┘
                        │
                        ▼
  ┌─────────────────────────────────────────────────┐
  │           Respond to Webhook                     │
  │        JSON { "respuesta": "..." }               │
  └─────────────────────┬───────────────────────────┘
                        │
                        ▼
  ┌─────────────────────────────────────────────────┐
  │         Respuesta al usuario ✅                  │
  └─────────────────────────────────────────────────┘
```

### Captura del Workflow en n8n

<img width="1226" height="718" alt="image" src="https://github.com/user-attachments/assets/21e0ee39-30f8-47d4-9419-6ed2f515b113" />


> *Nodos: Webhook → Execute a SQL query → AI Agent → Respond to Webhook*
> *Sub-nodos: OpenAI Chat Model, Simple Memory, HTTP Request (x2)*

---

### Infraestructura Cloud

```
AWS EC2
└── Docker
    ├── n8n (self-hosted)
    │   ├── Webhook endpoint
    │   ├── AI Agent + OpenAI Chat Model (NVIDIA NIM)
    │   ├── PostgreSQL Chat Memory
    │   └── HTTP Request Tools
    └── PostgreSQL
        ├── cosmos DB (estudiantes UNAB)
        └── pgvector (embeddings RAG)
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Versión | Rol |
|------|-----------|---------|-----|
| **Interfaz** | Streamlit | 1.x | Frontend del chatbot |
| **Orquestación** | n8n self-hosted | Latest | Workflows e integración |
| **LLM** | NVIDIA NIM — LLaMA 3.1 | 8B | Generación de respuestas |
| **Base de datos** | PostgreSQL — cosmos UNAB | 15 | Datos de estudiantes |
| **Memoria** | Simple Memory (n8n) | — | Historial de conversación |
| **Vectorial** | pgvector | 0.5+ | RAG embeddings |
| **Contenedor** | Docker | Latest | Despliegue del sistema |
| **Cloud** | AWS EC2 | — | Infraestructura servidor |
| **Calendario** | Google Sheets API | v4 | Eventos académicos CCD |
| **Scraping** | n8n HTTP Request | — | Noticias y cursos nuevos |
| **HTTP Client** | Python requests | 2.x | Comunicación con n8n |

---

## 🔄 Workflow en n8n

El sistema implementa un workflow principal con agente inteligente y herramientas especializadas:

### Nodos del workflow

| # | Nodo | Tipo | Función |
|---|------|------|---------|
| 1 | **Webhook** | Trigger | Recibe POST con pregunta e ID del estudiante |
| 2 | **Execute a SQL query** | Postgres | Consulta progreso real en BD cosmos UNAB |
| 3 | **AI Agent** | Agent | Orquesta la respuesta con LLM + tools |
| 4 | **OpenAI Chat Model** | LLM | LLaMA 3.1 8B via NVIDIA NIM API |
| 5 | **Simple Memory** | Memory | Mantiene historial de la conversación |
| 6 | **HTTP Request** | Tool | Consulta RAG / documentos institucionales |
| 7 | **HTTP Request1** | Tool | Consulta calendario Google Sheets |
| 8 | **Respond to Webhook** | Output | Devuelve JSON con la respuesta |

### Query SQL a la BD cosmos

```sql
SELECT
  e.nombre_completo,
  e.programa_academico,
  e.anio_ingreso,
  pe.pilar1_cumplido,
  pe.pilar2_cumplido,
  pe.pilar3_cumplido,
  pe.cursos_aprobados,
  pe.cursos_faltantes
FROM progreso_estudiante pe
JOIN estudiante e ON e.id_estudiante = pe.id_estudiante
WHERE pe.id_estudiante = '{{ $json.body.estudiante_id }}'
```

### System Prompt del AI Agent

```
Eres UNAB-Bot, asistente virtual del Centro de Competencias
Digitales (CCD) de la Universidad Autónoma de Bucaramanga.

RUTA CCD:
- Pilar 1 OBLIGATORIO: Interacción Digital
- Pilar 2 ELIGE 1: Narrativas Digitales, Visualización de
  Datos, Marca Personal Digital
- Pilar 3 ELIGE 1: IA Generativa, Legislación Digital,
  Bienestar Digital

INSIGNIA CCD: 3 pilares completados = 48 horas totales.

CALENDARIO:
- Inscripciones: 10 de marzo
- Prueba diagnóstica: 15 de marzo
- Inicio de cursos: 25 de marzo

Responde SIEMPRE en español, amable y conciso.
Usa los datos del estudiante para personalizar respuestas.
```

---

## 🎓 Ruta de Competencias Digitales

```
┌─────────────────┬─────────────────────┬─────────────────────┐
│    PILAR 1 🔵   │      PILAR 2 🟢     │      PILAR 3 🟠     │
│   OBLIGATORIO   │      ELIGE 1        │      ELIGE 1        │
├─────────────────┼─────────────────────┼─────────────────────┤
│                 │ Narrativas          │ IA Generativa       │
│  Interacción    │ Digitales           │                     │
│  Digital        │─────────────────────│ Legislación         │
│                 │ Visualización       │ Digital             │
│                 │ de Datos            │─────────────────────│
│                 │─────────────────────│ Bienestar           │
│                 │ Marca Personal      │ Digital             │
│                 │ Digital             │                     │
└─────────────────┴─────────────────────┴─────────────────────┘

🏅 INSIGNIA CCD = Pilar 1 + Pilar 2 + Pilar 3 = 48 horas
```

---

## 💻 Interfaz Web — Streamlit

### Captura de la aplicación

<img width="930" height="589" alt="image" src="https://github.com/user-attachments/assets/3599479a-7ba1-4f40-bec2-c4e4fc60d8dd" />


> <img width="1083" height="832" alt="image" src="https://github.com/user-attachments/assets/bb857018-5401-4fcd-9607-0f7a4f5ea7d4" />

### Características de la interfaz

```
app.py
├── 🎨 Estilos CSS personalizados
│   ├── Tema oscuro profesional
│   ├── Fuentes: Syne + DM Sans (Google Fonts)
│   └── Gradientes y colores institucionales
│
├── 📱 Sidebar
│   ├── Input de ID de estudiante
│   ├── Badge de estado de conexión
│   ├── Lista de capacidades del bot
│   └── Botón limpiar conversación
│
├── 💬 Área de chat
│   ├── Mensaje de bienvenida automático
│   ├── Historial con burbujas diferenciadas
│   ├── Input tipo ChatGPT
│   └── Spinner de carga
│
└── 🔌 Comunicación con n8n
    ├── requests.post() → webhook
    ├── Manejo de múltiples formatos de respuesta
    ├── Timeout de 30 segundos
    └── Mensajes de error descriptivos
```

---

## 🗄️ Base de Datos

### Conexión BD cosmos UNAB

```
Host:     unab-n8n.duckdns.org
Puerto:   5432
Base:     cosmos
Usuario:  ccd_reader
```

### Esquema de tablas

```sql
-- Información del estudiante
CREATE TABLE estudiante (
  id_estudiante      VARCHAR  PRIMARY KEY,
  nombre_completo    VARCHAR  NOT NULL,
  programa_academico VARCHAR,
  anio_ingreso       INTEGER
);

-- Progreso en la ruta CCD
CREATE TABLE progreso_estudiante (
  id_estudiante    VARCHAR  REFERENCES estudiante,
  pilar1_cumplido  BOOLEAN  DEFAULT FALSE,
  pilar2_cumplido  BOOLEAN  DEFAULT FALSE,
  pilar3_cumplido  BOOLEAN  DEFAULT FALSE,
  cursos_aprobados TEXT[],
  cursos_faltantes TEXT[]
);
```


---

## 🧠 Sistema RAG



<img width="288" height="333" alt="image" src="https://github.com/user-attachments/assets/c06ef755-493c-4e72-b311-94fff4726da8" />

El sistema RAG (Retrieval Augmented Generation) permite consultar documentos institucionales del CCD.

### Flujo de indexación

```
Documento PDF CCD
      │
      ▼
Chunking (~500 tokens por fragmento)
      │
      ▼
NVIDIA NIM Embeddings API
      │
      ▼
PostgreSQL + pgvector
```

### Flujo de consulta en tiempo real

```
Pregunta del usuario
      │
      ▼
Embedding de la pregunta
      │
      ▼
Búsqueda por similitud coseno (pgvector)
      │
      ▼
Top-3 fragmentos relevantes
      │
      ▼
LLM genera respuesta con contexto ✅
```



---

## 🚀 Instalación y Ejecución

### Requisitos

- Python 3.10+
- Cuenta en [NVIDIA Build](https://build.nvidia.com) con API Key `nvapi-...`
- Acceso al n8n: `unab-n8n.duckdns.org:5678`
- Acceso a BD cosmos UNAB

### Paso a paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/chatbot-ccd-unab.git
cd chatbot-ccd-unab

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py

# 4. Abrir en el navegador
# http://localhost:8501
```

### requirements.txt

```
streamlit
requests
psycopg2-binary
```

### Variables a configurar en app.py

```python
# URL del webhook de n8n
N8N_URL = "https://unab-n8n.duckdns.org:5678/webhook/chatbot-grupobien"
```

### Estructura del proyecto

```
chatbot-ccd-unab/
├── app.py              # Interfaz Streamlit
├── test.py             # Prueba del webhook
├── requirements.txt    # Dependencias
├── README.md           # Documentación
└── docs/
    ├── workflow-n8n.png
    ├── app-screenshot.png
    └── arquitectura.png
```

---

## 💬 Ejemplos de Interacción

### Consulta de cursos

```
👤 ¿Qué cursos debo tomar en competencias digitales?

🤖 Para completar la ruta CCD debes tomar:
   • Pilar 1 (Obligatorio): Interacción Digital
   • Pilar 2 (Elige 1): Narrativas Digitales,
     Visualización de Datos o Marca Personal Digital
   • Pilar 3 (Elige 1): IA Generativa,
     Legislación Digital o Bienestar Digital
```

---

### Consulta de progreso personal

```
👤 [ID: u171531] ¿Cuántos pilares me faltan para la insignia?

🤖 Hola! Según tu progreso en la BD de la UNAB:
   ✅ Pilar 1 — Interacción Digital: Completado
   ❌ Pilar 2 — Analítica: Pendiente
   ❌ Pilar 3 — Tecnologías: Pendiente

   ¡Te faltan 2 pilares para obtener tu insignia CCD! 🏅
```

---

### Consulta de calendario

```
👤 ¿Cuándo son las inscripciones?

🤖 Las inscripciones a cursos del CCD son el 10 de marzo.
   Luego debes presentar la prueba diagnóstica el 15 de marzo,
   que es obligatoria. Los cursos inician el 25 de marzo.
   ¿Necesitas ayuda con algo más?
```

---

### Consulta de insignia

```
👤 ¿Qué es la insignia CCD?

🤖 La Insignia CCD es una certificación oficial de la UNAB
   que reconoce tus competencias digitales. Para obtenerla
   debes completar los 3 pilares de la ruta con un total
   de 48 horas de formación. ¡Es un diferenciador importante
   en tu perfil profesional! 🏅
```

---

## 📊 Criterios de Evaluación

| Criterio | Peso | Estado |
|----------|------|--------|
| 🏗️ Arquitectura del sistema | **20%** | ✅ Implementado |
| 🧠 Implementación RAG | **20%** | ✅ Implementado |
| 🔄 Workflows n8n | **20%** | ✅ Implementado |
| 💻 Aplicación Streamlit | **20%** | ✅ Implementado |
| 🗄️ Base de datos | **10%** | ✅ Implementado |
| 📄 Documentación técnica | **10%** | ✅ Este README |
| **Total** | **100%** | ✅ |

---

## 👥 Equipo

| Nombre | Rol |
|--------|-----|
| **Juan David Amaya Quintero** | Desarrollador principal — Streamlit + n8n |
| **Efrain Alvarez Lobo** | Arquitectura del sistema — BD + RAG |
| **Andres Felipe Quiñones** | Workflows n8n + Integración NVIDIA |

---

## 📄 Licencia

Proyecto académico desarrollado para el curso de **Ciencia de Datos**  
**Universidad Autónoma de Bucaramanga — UNAB**  
**Centro de Competencias Digitales — CCD**  
**2026**

---

<div align="center">

**Hecho con ❤️ por el Grupo CCD — UNAB**

**PROFESOR: ALFREDO DIAZ**

[![UNAB](https://img.shields.io/badge/UNAB-Bucaramanga-1B2A4A?style=flat-square)](https://unab.edu.co)
[![CCD](https://img.shields.io/badge/Centro_de_Competencias-Digitales-2563EB?style=flat-square)](https://unab.edu.co)

</div>

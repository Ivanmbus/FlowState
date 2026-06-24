# Reproductor de Música con IA — Hoja de Ruta y Arquitectura

## 1. Resumen de la idea

Aplicación multiplataforma (escritorio + móvil) para:
- Buscar, importar/descargar y organizar canciones.
- Crear y gestionar playlists.
- Perfil de usuario con estadísticas de escucha.
- Asistente de IA que recomienda canciones y genera playlists a partir de peticiones en lenguaje natural.
- Modo "público" opcional, en el que **no se descargan canciones de internet**, sino que el usuario importa sus propios archivos MP3 (biblioteca local subida por el propio usuario).

## 2. Nota legal importante (léelo antes de programar nada)

La descarga automática de canciones desde plataformas de streaming o de internet en general **infringe derechos de autor** en la gran mayoría de los casos, incluso para uso personal, y es **mucho más grave** si la app se hace pública (responsabilidad por distribución de contenido protegido).

Recomendación de diseño legal:

| Modo | Qué se permite | Fuente de las canciones |
|---|---|---|
| **Privado (tú)** | Descarga/importación flexible | Tu propia música, servicios con licencia API (ver abajo), archivos que ya posees |
| **Público (otros usuarios)** | Solo importación manual de MP3 | El usuario sube sus propios archivos; la app nunca descarga ni distribuye contenido de terceros |

Fuentes de audio recomendadas y legales para la búsqueda/descarga "real":
- **Jamendo API** y **Free Music Archive**: música con licencias libres, descarga legal.
- **APIs de streaming (Spotify Web API, YouTube Music, Deezer)**: permiten *buscar metadatos, reproducir vía SDK embebido o enlazar*, pero **no permiten descargar el audio** bajo sus términos de servicio. Úsalas para la búsqueda/reproducción, no para descarga.
- **Tu propia colección**: importas tus MP3 (comprados o de tu propiedad) directamente.

Diseño técnico sugerido: separar claramente el módulo `ingestion` en dos proveedores:
- `LocalImportProvider` (arrastrar/subir MP3 propios) → disponible en modo público y privado.
- `LicensedSourceProvider` (Jamendo, FMA, etc.) → solo en modo privado, con flag de "fuente con licencia libre".

Esto te permite cumplir la ley sin perder funcionalidad real.

## 3. Arquitectura general (visión de alto nivel)

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│   Cliente Móvil (iOS/And.)  │     │   Cliente Escritorio         │
│   Flutter / React Native    │     │   Electron + React, o Tauri  │
└──────────────┬───────────────┘     └──────────────┬───────────────┘
               │                                    │
               └───────────────┬────────────────────┘
                                │ HTTPS / WebSocket
                       ┌────────▼────────┐
                       │   API Gateway    │  (FastAPI)
                       └────────┬────────┘
        ┌───────────────┬───────┼────────────────┬───────────────┐
        │               │       │                │               │
 ┌──────▼─────┐  ┌──────▼─────┐ │        ┌────────▼───────┐ ┌─────▼──────┐
 │ Auth Service│  │ Music Mgmt │ │        │ AI Assistant   │ │ Stats Svc  │
 │ (FastAPI)   │  │ Service     │ │        │ Service        │ │ (FastAPI)  │
 └──────┬─────┘  └──────┬─────┘ │        └────────┬───────┘ └─────┬──────┘
        │               │       │                 │               │
        │        ┌──────▼───────▼───┐      ┌───────▼───────┐       │
        │        │  PostgreSQL DB   │      │ Claude API /  │       │
        │        │ (usuarios,       │      │ vector store  │       │
        │        │ canciones,       │      │ (embeddings)  │       │
        │        │ playlists)       │      └───────────────┘       │
        │        └──────────────────┘                              │
        │                                                          │
 ┌──────▼─────┐                                            ┌───────▼──────┐
 │ Object      │  (Audio files / portadas)                 │ Redis Cache  │
 │ Storage     │  S3 / MinIO                                │ (sesiones,   │
 │ (S3/MinIO)  │                                             │ stats live) │
 └─────────────┘                                            └──────────────┘
```

## 4. Stack tecnológico recomendado

### 4.1 Frontend

| Capa | Tecnología | Por qué |
|---|---|---|
| Móvil + Escritorio (un solo código) | **Flutter** | Un único codebase real para Android, iOS, Windows, macOS, Linux. Buen rendimiento para audio y UI animada. |
| Alternativa si prefieres web tech | **React Native** (móvil) + **Tauri o Electron** (escritorio, reutilizando componentes React/Next.js) | Aprovechas conocimientos de Next.js que ya tienes. Tauri es más ligero que Electron. |
| Reproducción de audio | `just_audio` (Flutter) o `react-native-track-player` / `howler.js` (web) | Soporte de streaming, colas, control en segundo plano. |

**Recomendación concreta**: dado tu stack actual (Next.js, FastAPI), te sugiero **Tauri + React/Next.js** para escritorio y **React Native** para móvil, compartiendo lógica de negocio en un paquete TypeScript común (`packages/core`). Si prefieres minimizar mantenimiento de dos bases de UI, Flutter es la opción más eficiente a largo plazo aunque tengas que aprender Dart.

### 4.2 Backend

| Componente | Tecnología | Detalle |
|---|---|---|
| API principal | **FastAPI** (Python) | Ya lo conoces; ideal para servicios REST + WebSocket. |
| Autenticación | **FastAPI + OAuth2/JWT**, o **Auth0/Clerk** si quieres ahorrar tiempo | Login propio, Google, Apple. |
| Base de datos relacional | **PostgreSQL** | Usuarios, canciones, playlists, relaciones, estadísticas agregadas. |
| Búsqueda de canciones (metadatos) | **PostgreSQL full-text search** o **Meilisearch/Elasticsearch** si la biblioteca crece mucho | Búsqueda rápida por título/artista/álbum. |
| Caché y sesiones | **Redis** | Estado de reproducción en vivo, contadores de estadísticas, rate limiting. |
| Almacenamiento de audio | **S3 compatible (AWS S3 o MinIO self-hosted)** | Archivos MP3 importados y portadas. |
| Cola de tareas (procesado de audio, generación de playlists IA) | **Celery + Redis** o **RQ** | Procesar metadatos (ID3 tags), generar embeddings, tareas largas sin bloquear la API. |
| Contenedores / despliegue | **Docker + Docker Compose**, CI/CD con **GitHub Actions** | Coherente con tu experiencia previa. |

### 4.3 Asistente de IA

| Función | Enfoque técnico |
|---|---|
| Recomendación de canciones | **Embeddings de audio/metadatos** (ej. usando características de audio + texto: género, artista, letra) almacenados en una base vectorial (**pgvector** sobre PostgreSQL, o **Qdrant/Chroma** si quieres algo dedicado). |
| Generación de playlists por lenguaje natural | Llamada a la **API de Claude** (Anthropic) con function calling: el usuario pide "playlist relajante de noche" → Claude interpreta intención → consulta tu base de canciones filtrando por género/tempo/mood → devuelve la lista estructurada en JSON. |
| Arquitectura del asistente | Microservicio independiente (`ai-assistant-service`) que: 1) recibe la petición en texto, 2) construye un prompt con el catálogo disponible (o usa RAG sobre tu base vectorial), 3) llama a Claude con `tool_use` para devolver una estructura `{playlist_name, tracks: [...]}`, 4) guarda el resultado como playlist nueva. |
| Dato clave | No necesitas entrenar un modelo propio: con prompting + RAG sobre tus propios metadatos es suficiente para una app personal. |

### 4.4 Estadísticas de perfil

- Eventos de escucha (`play_started`, `play_completed`, `skipped`) enviados al backend vía WebSocket o REST.
- Agregación periódica (cron/Celery beat) calculando: canción más escuchada, tiempo total, géneros favoritos, rachas de escucha.
- Tablas: `listening_events` (raw) → `user_stats_daily` (agregado) para no recalcular todo siempre.

### 4.5 Importación de MP3 (modo público)

- Endpoint de subida (`POST /tracks/import`) que acepta MP3, extrae metadatos con **Mutagen** (Python) o **music-metadata** (JS), guarda el archivo en almacenamiento de objetos asociado solo al usuario que lo subió.
- Importante: en modo público, cada usuario solo puede reproducir/gestionar **sus propios** archivos subidos; no hay compartición de audio entre usuarios (evita problemas legales de distribución).

## 5. Modelo de datos (simplificado)

```
users (id, email, password_hash, display_name, mode[private|public], created_at)
tracks (id, owner_id, title, artist, album, duration, source[local|jamendo|...], storage_url, cover_url)
playlists (id, owner_id, name, description, created_by_ai[bool], created_at)
playlist_tracks (playlist_id, track_id, position)
listening_events (id, user_id, track_id, event_type, timestamp)
user_stats_daily (user_id, date, total_minutes, top_genre, top_track_id)
ai_requests (id, user_id, prompt, generated_playlist_id, created_at)
```

## 6. Fases de desarrollo recomendadas

### Fase 1 — Núcleo (MVP privado)
1. Backend FastAPI con auth, modelo de datos, CRUD de tracks/playlists.
2. Importación local de MP3 + extracción de metadatos.
3. Reproductor básico en un solo cliente (empieza por escritorio o móvil, no ambos a la vez).
4. Perfil con estadísticas simples (canciones más escuchadas).

### Fase 2 — Multiplataforma
5. Extender UI al segundo cliente (móvil o escritorio, el que falte).
6. Sincronización de estado de reproducción y playlists entre dispositivos (vía API).

### Fase 3 — IA
7. Generar embeddings de tu catálogo (género, mood, tempo si lo extraes con librerías como `librosa`).
8. Integrar Claude API con function calling para generación de playlists por texto.
9. Sistema de recomendación básico (similaridad de embeddings + historial de escucha).

### Fase 4 — Fuentes legales adicionales (solo modo privado)
10. Integrar Jamendo/FMA como `LicensedSourceProvider` para descarga real ampliando tu biblioteca.

### Fase 5 — Modo público
11. Sistema de roles/permisos (privado vs público).
12. Aislamiento de bibliotecas por usuario, sin descarga automática, solo importación manual.
13. Hardening de seguridad (rate limiting, validación de archivos, escaneo antivirus de uploads, cumplimiento de RGPD si vas a tener usuarios reales en la UE).

## 7. Consideraciones de seguridad y cumplimiento (RGPD, ya que estás en España/UE)

- Si el modo público llega a tener usuarios reales, necesitarás: política de privacidad, consentimiento explícito, derecho al olvido (borrar cuenta y datos), y minimizar datos personales almacenados.
- Cifrado de contraseñas con `bcrypt`/`argon2`, JWT con expiración corta + refresh tokens.
- Validar tipo real de archivo subido (no fiarte de la extensión) antes de aceptarlo como MP3.

## 8. Resumen de stack final sugerido

```
Frontend:   Tauri + Next.js (escritorio) / React Native (móvil)
Backend:    FastAPI + PostgreSQL + Redis + Celery
Almacenamiento: S3 / MinIO
IA:         Claude API (function calling) + pgvector para embeddings
Infra:      Docker Compose → CI/CD GitHub Actions
```

Este stack reutiliza directamente tu experiencia previa (FastAPI, Next.js, Docker, CI/CD, SQL) y añade solo lo nuevo imprescindible (Celery, pgvector, integración con Claude API), lo que te permite avanzar rápido sin partir de cero.
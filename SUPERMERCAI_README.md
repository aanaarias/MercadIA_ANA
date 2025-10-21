# 🛒 SupermercAI - Generador de Menús Semanales

Aplicación web FastAPI para generar menús semanales personalizados y vincularlos directamente con el carrito de la compra del supermercado.

## 🎯 Características principales

- ✅ **Generación de menús personalizados** basados en objetivos nutricionales
- ✅ **Edición individual de recetas** dentro del menú semanal
- ✅ **Integración automática con carrito** de compra
- ✅ **Dashboard de recetas guardadas** (próximamente)
- ✅ **Sistema de aprendizaje** basado en preferencias (próximamente)

## 📁 Estructura del proyecto

```
SUPERMERCAI/
├── static/                 # Archivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos principales
│   ├── js/
│   │   └── script.js      # Lógica del frontend
│   └── img/               # Imágenes (añadir manualmente)
├── templates/             # Templates HTML
│   └── index.html         # Página principal
├── main.py                # Punto de entrada FastAPI
├── requirements.txt       # Dependencias Python
├── SUPERMERCAI_README.md  # Este archivo
```

## 🚀 Instalación y ejecución

### 1. Clonar o descargar el proyecto

```bash
# Descargar todos los archivos del proyecto
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en: **http://localhost:8000**

## 🔧 Endpoints de la API

### Página principal
- `GET /` - Renderiza la interfaz principal

### APIs REST
- `GET /api/hello` - Endpoint de prueba
- `POST /api/generar-menu` - Genera un menú semanal personalizado
- `POST /api/regenerar-receta` - Regenera una receta individual
- `POST /api/agregar-a-carrito` - Convierte recetas en items del carrito
- `GET /api/receta/{id}` - Obtiene detalles de una receta
- `GET /api/recetas-guardadas` - Lista recetas guardadas del usuario

### Ejemplo de uso con `curl`

```bash
# Test endpoint
curl http://localhost:8000/api/hello

# Generar menú
curl -X POST http://localhost:8000/api/generar-menu \
  -H "Content-Type: application/json" \
  -d '{
    "objetivo": "comer_sano",
    "tiempo_cocina": "medio",
    "num_personas": 2,
    "presupuesto": 50,
    "estilo_cocina": "mediterranea",
    "preferencia_marca": "marca_blanca"
  }'
```

## 🎨 Personalización

### Añadir más recetas

Edita el array `RECETAS_EJEMPLO` en `main.py`:

```python
RECETAS_EJEMPLO = [
    {
        "id": 4,
        "nombre": "Tu nueva receta",
        "descripcion": "...",
        # ... más campos
    }
]
```

### Cambiar estilos

Los estilos están centralizados con variables CSS en `static/css/style.css`:

```css
:root {
  --color-primary: #2563eb;
  --color-secondary: #10b981;
  /* ... más variables */
}
```

### Integrar con IA (OpenAI/Claude)

1. Descomentar dependencias en `requirements.txt`
2. Añadir tu API key en archivo `.env`:
   ```
   OPENAI_API_KEY=tu-key-aqui
   ```
3. Modificar función `generar_menu()` en `main.py`

## 📦 Próximas funcionalidades

- [ ] Integración con API de OpenAI para generar recetas reales
- [ ] Base de datos PostgreSQL para persistencia
- [ ] Sistema de autenticación de usuarios
- [ ] Dashboard de recetas guardadas completo
- [ ] Sistema de reseñas y valoraciones
- [ ] Ajuste dinámico de porciones
- [ ] Machine Learning para recomendaciones

## 🐛 Debugging

```bash
# Ver logs detallados
uvicorn main:app --reload --log-level debug

# Verificar dependencias instaladas
pip list
```

## 📄 Licencia

Este proyecto es un MVP educativo desarrollado con fines de prototipado rápido.

---

**Desarrollado con FastAPI y ❤️**

"""
SUPERMERCAI - Generador de Menús Semanales
FastAPI Backend Application
"""

from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Inicializar FastAPI
app = FastAPI(
    title="SupermercAI",
    description="API para generación de menús semanales personalizados",
    version="1.0.0"
)

# Configurar carpetas estáticas y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ==================== MODELOS DE DATOS ====================

class UserPreferences(BaseModel):
    """Preferencias del usuario para generar el menú"""
    objetivo: str  # "ganar_masa", "definir", "adelgazar", "comer_sano"
    tiempo_cocina: str  # "poco", "medio", "mucho"
    alergias: Optional[List[str]] = []
    num_personas: int = 2
    presupuesto: float = 50.0
    estilo_cocina: str = "mediterranea"  # "mediterranea", "asiatica", "vegetariana"
    preferencia_marca: str = "marca_blanca"  # "marca_blanca", "otras"

class Recipe(BaseModel):
    """Modelo de receta individual"""
    id: int
    nombre: str
    descripcion: str
    tiempo_preparacion: int
    calorias: int
    imagen_url: str
    ingredientes: List[dict]
    pasos: List[str]
    tipo_comida: str  # "desayuno", "comida", "cena"

class WeeklyMenu(BaseModel):
    """Menú semanal completo"""
    user_id: Optional[int] = None
    preferencias: UserPreferences
    recetas: List[Recipe]
    costo_total: float

class CartItem(BaseModel):
    """Item del carrito de compra"""
    producto_id: int
    nombre: str
    cantidad: float
    unidad: str
    precio: float
    receta_id: int

# ==================== DATOS DE EJEMPLO ====================

RECETAS_EJEMPLO = [
    {
        "id": 1,
        "nombre": "Pollo al Horno con Verduras",
        "descripcion": "Pechuga de pollo jugosa con verduras asadas",
        "tiempo_preparacion": 45,
        "calorias": 450,
        "imagen_url": "/static/img/pollo-verduras.jpg",
        "tipo_comida": "cena",
        "ingredientes": [
            {"nombre": "Pechuga de pollo", "cantidad": 400, "unidad": "g", "producto_id": 1, "precio": 4.50},
            {"nombre": "Pimientos", "cantidad": 2, "unidad": "unidades", "producto_id": 2, "precio": 1.80},
            {"nombre": "Calabacín", "cantidad": 1, "unidad": "unidad", "producto_id": 3, "precio": 0.90},
            {"nombre": "Aceite de oliva", "cantidad": 3, "unidad": "cucharadas", "producto_id": 4, "precio": 0.30}
        ],
        "pasos": [
            "Precalentar el horno a 200°C",
            "Cortar las verduras en trozos medianos",
            "Sazonar el pollo con sal, pimienta y hierbas",
            "Colocar todo en una bandeja de horno",
            "Hornear durante 35-40 minutos"
        ]
    },
    {
        "id": 2,
        "nombre": "Ensalada César con Pollo",
        "descripcion": "Fresca ensalada con pollo a la plancha",
        "tiempo_preparacion": 20,
        "calorias": 380,
        "imagen_url": "/static/img/ensalada-cesar.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Lechuga romana", "cantidad": 1, "unidad": "unidad", "producto_id": 5, "precio": 1.20},
            {"nombre": "Pechuga de pollo", "cantidad": 200, "unidad": "g", "producto_id": 1, "precio": 2.25},
            {"nombre": "Queso parmesano", "cantidad": 50, "unidad": "g", "producto_id": 6, "precio": 1.50},
            {"nombre": "Pan tostado", "cantidad": 100, "unidad": "g", "producto_id": 7, "precio": 0.80}
        ],
        "pasos": [
            "Cocinar el pollo a la plancha",
            "Lavar y trocear la lechuga",
            "Preparar los picatostes con el pan",
            "Mezclar con salsa césar",
            "Añadir queso parmesano rallado"
        ]
    },
    {
        "id": 3,
        "nombre": "Pasta con Salsa de Tomate Casera",
        "descripcion": "Pasta italiana con salsa de tomate natural",
        "tiempo_preparacion": 30,
        "calorias": 520,
        "imagen_url": "/static/img/pasta-tomate.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Pasta", "cantidad": 300, "unidad": "g", "producto_id": 8, "precio": 1.20},
            {"nombre": "Tomate triturado", "cantidad": 400, "unidad": "g", "producto_id": 9, "precio": 0.90},
            {"nombre": "Ajo", "cantidad": 2, "unidad": "dientes", "producto_id": 10, "precio": 0.10},
            {"nombre": "Albahaca fresca", "cantidad": 1, "unidad": "manojo", "producto_id": 11, "precio": 1.50}
        ],
        "pasos": [
            "Hervir agua con sal para la pasta",
            "Sofreír ajo en aceite de oliva",
            "Añadir el tomate triturado y cocinar 15 min",
            "Cocinar la pasta al dente",
            "Mezclar pasta con salsa y albahaca"
        ]
    }
]

# ==================== RUTAS ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/hello")
async def hello_api():
    """Endpoint de ejemplo que devuelve JSON"""
    return {
        "message": "¡Bienvenido a SupermercAI!",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/api/generar-menu")
async def generar_menu(preferencias: UserPreferences):
    """
    Genera un menú semanal personalizado basado en las preferencias del usuario
    
    En producción, aquí se integraría con:
    - API de OpenAI para generar recetas con IA
    - Base de datos de recetas del supermercado
    - Sistema de recomendación basado en historial
    """
    try:
        # Simular generación de menú (7 cenas)
        menu_semanal = []
        costo_total = 0.0
        
        # Seleccionar recetas según preferencias
        for dia in range(7):
            # En producción: aquí iría la lógica de IA/ML
            receta = RECETAS_EJEMPLO[dia % len(RECETAS_EJEMPLO)].copy()
            receta["dia"] = dia + 1
            
            # Calcular costo de ingredientes
            costo_receta = sum(ing["precio"] for ing in receta["ingredientes"])
            costo_total += costo_receta
            
            menu_semanal.append(receta)
        
        return {
            "success": True,
            "menu": {
                "recetas": menu_semanal,
                "costo_total": round(costo_total, 2),
                "preferencias": preferencias.dict()
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/regenerar-receta")
async def regenerar_receta(dia: int, preferencias: UserPreferences):
    """
    Regenera una receta individual del menú
    """
    try:
        # Seleccionar una receta diferente
        receta_nueva = RECETAS_EJEMPLO[(dia + 1) % len(RECETAS_EJEMPLO)].copy()
        receta_nueva["dia"] = dia
        
        return {
            "success": True,
            "receta": receta_nueva
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agregar-a-carrito")
async def agregar_a_carrito(recetas_ids: List[int] = Body(..., embed=True)):
    carrito = {}

    for receta_id in recetas_ids:
        receta = next((r for r in RECETAS_EJEMPLO if r["id"] == receta_id), None)
        if not receta:
            continue

        for ing in receta["ingredientes"]:
            key = str(ing["producto_id"])
            if key in carrito:
                carrito[key]["cantidad"] += ing["cantidad"]
                carrito[key]["precio"] += ing["precio"]
                # (opcional) registrar en qué recetas aparece:
                carrito[key]["recetas"].append(receta_id)
            else:
                carrito[key] = {
                    "producto_id": ing["producto_id"],
                    "nombre": ing["nombre"],
                    "cantidad": ing["cantidad"],
                    "unidad": ing["unidad"],
                    "precio": ing["precio"],
                    "recetas": [receta_id],
                }

    items_carrito = list(carrito.values())
    total = round(sum(item["precio"] for item in items_carrito), 2)
    return {"success": True, "carrito": {"items": items_carrito, "total": total, "num_items": len(items_carrito)}}


@app.get("/api/receta/{receta_id}")
async def obtener_receta(receta_id: int):
    """Obtiene los detalles completos de una receta"""
    receta = next((r for r in RECETAS_EJEMPLO if r["id"] == receta_id), None)
    
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    return {"success": True, "receta": receta}

@app.get("/api/recetas-guardadas")
async def recetas_guardadas(user_id: Optional[int] = None):
    """
    Obtiene las recetas guardadas del usuario
    En producción: consultar base de datos
    """
    return {
        "success": True,
        "recetas": RECETAS_EJEMPLO,
        "total": len(RECETAS_EJEMPLO)
    }

# ==================== EJECUCIÓN ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

"""
SUPERMERCAI - Generador de Menús Semanales
FastAPI Backend Application
"""

from fastapi import FastAPI, Request, HTTPException
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
    },
    {
        "id": 4,
        "nombre": "Tortilla de Espinacas",
        "descripcion": "Tortilla ligera con espinacas frescas",
        "tiempo_preparacion": 15,
        "calorias": 250,
        "imagen_url": "/static/img/tortilla-espinacas.jpg",
        "tipo_comida": "desayuno",
        "ingredientes": [
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unidades", "producto_id": 12, "precio": 0.75},
            {"nombre": "Espinacas frescas", "cantidad": 100, "unidad": "g", "producto_id": 13, "precio": 1.00},
            {"nombre": "Aceite de oliva", "cantidad": 1, "unidad": "cucharada", "producto_id": 4, "precio": 0.10}
        ],
        "pasos": [
            "Batir los huevos en un bol",
            "Saltear las espinacas en aceite",
            "Añadir los huevos y cocinar a fuego medio",
            "Doblar la tortilla y servir caliente"
        ]
    },
    {
        "id": 5,
        "nombre": "Crema de Calabaza",
        "descripcion": "Sopa cremosa de calabaza con toque de jengibre",
        "tiempo_preparacion": 35,
        "calorias": 300,
        "imagen_url": "/static/img/crema-calabaza.jpg",
        "tipo_comida": "cena",
        "ingredientes": [
            {"nombre": "Calabaza", "cantidad": 500, "unidad": "g", "producto_id": 14, "precio": 2.00},
            {"nombre": "Cebolla", "cantidad": 1, "unidad": "unidad", "producto_id": 15, "precio": 0.40},
            {"nombre": "Jengibre", "cantidad": 10, "unidad": "g", "producto_id": 16, "precio": 0.30},
            {"nombre": "Caldo de verduras", "cantidad": 500, "unidad": "ml", "producto_id": 17, "precio": 0.80}
        ],
        "pasos": [
            "Pelar y cortar la calabaza y cebolla",
            "Saltear con jengibre en una olla",
            "Añadir el caldo y cocinar 25 minutos",
            "Triturar hasta obtener una crema suave"
        ]
    },
    {
        "id": 6,
        "nombre": "Yogur con Frutas y Miel",
        "descripcion": "Desayuno saludable con frutas frescas",
        "tiempo_preparacion": 10,
        "calorias": 200,
        "imagen_url": "/static/img/yogur-frutas.jpg",
        "tipo_comida": "desayuno",
        "ingredientes": [
            {"nombre": "Yogur natural", "cantidad": 150, "unidad": "g", "producto_id": 18, "precio": 0.60},
            {"nombre": "Frutas variadas", "cantidad": 100, "unidad": "g", "producto_id": 19, "precio": 1.20},
            {"nombre": "Miel", "cantidad": 1, "unidad": "cucharada", "producto_id": 20, "precio": 0.40}
        ],
        "pasos": [
            "Colocar el yogur en un bol",
            "Añadir las frutas troceadas",
            "Rociar con miel al gusto"
        ]
    },
    {
        "id": 7,
        "nombre": "Arroz con Pollo",
        "descripcion": "Plato tradicional con arroz y pollo",
        "tiempo_preparacion": 40,
        "calorias": 550,
        "imagen_url": "/static/img/arroz-pollo.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Arroz", "cantidad": 200, "unidad": "g", "producto_id": 21, "precio": 0.90},
            {"nombre": "Muslos de pollo", "cantidad": 400, "unidad": "g", "producto_id": 22, "precio": 3.50},
            {"nombre": "Pimiento rojo", "cantidad": 1, "unidad": "unidad", "producto_id": 2, "precio": 0.90},
            {"nombre": "Caldo de pollo", "cantidad": 500, "unidad": "ml", "producto_id": 23, "precio": 1.00}
        ],
        "pasos": [
            "Dorar el pollo en una cazuela",
            "Añadir el pimiento troceado",
            "Incorporar el arroz y el caldo",
            "Cocinar a fuego medio hasta que el arroz esté listo"
        ]
    },
    {
        "id": 8,
        "nombre": "Salmón a la Plancha con Limón",
        "descripcion": "Salmón jugoso con toque cítrico",
        "tiempo_preparacion": 20,
        "calorias": 400,
        "imagen_url": "/static/img/salmon-limon.jpg",
        "tipo_comida": "cena",
        "ingredientes": [
            {"nombre": "Filete de salmón", "cantidad": 250, "unidad": "g", "producto_id": 24, "precio": 4.00},
            {"nombre": "Limón", "cantidad": 1, "unidad": "unidad", "producto_id": 25, "precio": 0.50},
            {"nombre": "Aceite de oliva", "cantidad": 1, "unidad": "cucharada", "producto_id": 4, "precio": 0.10}
        ],
        "pasos": [
            "Calentar la plancha con aceite",
            "Cocinar el salmón por ambos lados",
            "Añadir jugo de limón al final"
        ]
    },
    {
        "id": 9,
        "nombre": "Tostadas con Aguacate",
        "descripcion": "Tostadas crujientes con aguacate cremoso",
        "tiempo_preparacion": 10,
        "calorias": 300,
        "imagen_url": "/static/img/tostadas-aguacate.jpg",
        "tipo_comida": "desayuno",
        "ingredientes": [
            {"nombre": "Pan integral", "cantidad": 2, "unidad": "rebanadas", "producto_id": 26, "precio": 0.60},
            {"nombre": "Aguacate", "cantidad": 1, "unidad": "unidad", "producto_id": 27, "precio": 1.20},
            {"nombre": "Sal", "cantidad": 1, "unidad": "pizca", "producto_id": 28, "precio": 0.05}
        ],
        "pasos": [
            "Tostar el pan",
            "Machacar el aguacate y sazonar",
            "Untar sobre las tostadas"
        ]
    },
    {
        "id": 10,
        "nombre": "Lentejas con Verduras",
        "descripcion": "Plato nutritivo de lentejas con vegetales",
        "tiempo_preparacion": 50,
        "calorias": 480,
        "imagen_url": "/static/img/lentejas-verduras.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Lentejas", "cantidad": 300, "unidad": "g", "producto_id": 29, "precio": 1.50},
            {"nombre": "Zanahoria", "cantidad": 2, "unidad": "unidades", "producto_id": 30, "precio": 0.80},
            {"nombre": "Cebolla", "cantidad": 1, "unidad": "unidad", "producto_id": 15, "precio": 0.40},
            {"nombre": "Pimiento verde", "cantidad": 1, "unidad": "unidad", "producto_id": 31, "precio": 0.70}
        ],
        "pasos": [
            "Picar las verduras y sofreír",
            "Añadir las lentejas y agua",
            "Cocinar a fuego medio durante 40 minutos"
        ]
    },
    {
        "id": 11,
        "nombre": "Batido de Plátano y Avena",
        "descripcion": "Bebida energética para empezar el día",
        "tiempo_preparacion": 5,
        "calorias": 220,
        "imagen_url": "/static/img/batido-platano.jpg",
        "tipo_comida": "desayuno",
        "ingredientes": [
            {"nombre": "Plátano", "cantidad": 1, "unidad": "unidad", "producto_id": 32, "precio": 0.40},
            {"nombre": "Leche", "cantidad": 200, "unidad": "ml", "producto_id": 33, "precio": 0.50},
            {"nombre": "Avena", "cantidad": 30, "unidad": "g", "producto_id": 34, "precio": 0.20}
        ],
        "pasos": [
            "Colocar todos los ingredientes en la licuadora",
            "Batir hasta obtener una mezcla homogénea",
            "Servir frío"
        ]
    },
    {
        "id": 12,
        "nombre": "Pizza Casera de Verduras",
        "descripcion": "Pizza con base casera y vegetales frescos",
        "tiempo_preparacion": 60,
        "calorias": 600,
        "imagen_url": "/static/img/pizza-verduras.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Masa para pizza", "cantidad": 1, "unidad": "unidad", "producto_id": 35, "precio": 1.50},
            {"nombre": "Tomate frito", "cantidad": 100, "unidad": "g", "producto_id": 36, "precio": 0.60},
            {"nombre": "Mozzarella", "cantidad": 150, "unidad": "g", "producto_id": 37, "precio": 2.00},
            {"nombre": "Verduras variadas", "cantidad": 150, "unidad": "g", "producto_id": 38, "precio": 1.50}
        ],
        "pasos": [
            "Extender la masa en una bandeja",
            "Cubrir con tomate, queso y verduras",
            "Hornear a 200°C durante 25 minutos"
        ]
    },
    {
        "id": 13,
        "nombre": "Wrap de Pollo y Vegetales",
        "descripcion": "Wrap ligero con pollo a la plancha y verduras frescas",
        "tiempo_preparacion": 25,
        "calorias": 350,
        "imagen_url": "/static/img/wrap-pollo.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Tortilla de trigo", "cantidad": 2, "unidad": "unidades", "producto_id": 39, "precio": 1.00},
            {"nombre": "Pechuga de pollo", "cantidad": 200, "unidad": "g", "producto_id": 1, "precio": 2.25},
            {"nombre": "Lechuga", "cantidad": 50, "unidad": "g", "producto_id": 5, "precio": 0.60},
            {"nombre": "Tomate", "cantidad": 1, "unidad": "unidad", "producto_id": 40, "precio": 0.50}
        ],
        "pasos": [
            "Cocinar el pollo a la plancha y cortar en tiras",
            "Lavar y cortar las verduras",
            "Colocar todo sobre la tortilla",
            "Enrollar el wrap y servir"
        ]
    },
    {
        "id": 14,
        "nombre": "Crepes de Avena con Frutas",
        "descripcion": "Crepes saludables con avena y frutas frescas",
        "tiempo_preparacion": 30,
        "calorias": 280,
        "imagen_url": "/static/img/crepes-avena.jpg",
        "tipo_comida": "desayuno",
        "ingredientes": [
            {"nombre": "Harina de avena", "cantidad": 100, "unidad": "g", "producto_id": 34, "precio": 0.40},
            {"nombre": "Leche", "cantidad": 200, "unidad": "ml", "producto_id": 33, "precio": 0.50},
            {"nombre": "Huevos", "cantidad": 2, "unidad": "unidades", "producto_id": 12, "precio": 0.50},
            {"nombre": "Frutas variadas", "cantidad": 100, "unidad": "g", "producto_id": 19, "precio": 1.20}
        ],
        "pasos": [
            "Mezclar harina, leche y huevos",
            "Cocinar los crepes en una sartén antiadherente",
            "Rellenar con frutas frescas",
            "Doblar y servir"
        ]
    },
    {
        "id": 15,
        "nombre": "Hamburguesa Vegetal",
        "descripcion": "Hamburguesa casera con base de legumbres",
        "tiempo_preparacion": 40,
        "calorias": 420,
        "imagen_url": "/static/img/hamburguesa-vegetal.jpg",
        "tipo_comida": "comida",
        "ingredientes": [
            {"nombre": "Garbanzos cocidos", "cantidad": 200, "unidad": "g", "producto_id": 41, "precio": 1.00},
            {"nombre": "Pan de hamburguesa", "cantidad": 2, "unidad": "unidades", "producto_id": 42, "precio": 1.20},
            {"nombre": "Zanahoria", "cantidad": 1, "unidad": "unidad", "producto_id": 30, "precio": 0.40},
            {"nombre": "Cebolla", "cantidad": 1, "unidad": "unidad", "producto_id": 15, "precio": 0.40}
        ],
        "pasos": [
            "Triturar los garbanzos con zanahoria y cebolla",
            "Formar hamburguesas y cocinar en sartén",
            "Montar en el pan con tus toppings favoritos"
        ]
    },
    {
        "id": 16,
        "nombre": "Sopa de Fideos",
        "descripcion": "Sopa reconfortante con fideos finos",
        "tiempo_preparacion": 30,
        "calorias": 320,
        "imagen_url": "/static/img/sopa-fideos.jpg",
        "tipo_comida": "cena",
        "ingredientes": [
            {"nombre": "Fideos finos", "cantidad": 100, "unidad": "g", "producto_id": 43, "precio": 0.60},
            {"nombre": "Caldo de pollo", "cantidad": 500, "unidad": "ml", "producto_id": 23, "precio": 1.00},
            {"nombre": "Zanahoria", "cantidad": 1, "unidad": "unidad", "producto_id": 30, "precio": 0.40},
            {"nombre": "Puerro", "cantidad": 1, "unidad": "unidad", "producto_id": 44, "precio": 0.70}
        ],
        "pasos": [
            "Cortar las verduras y sofreír ligeramente",
            "Añadir el caldo y llevar a ebullición",
            "Incorporar los fideos y cocinar 10 minutos",
            "Servir caliente"
        ]
    },
    {
        "id": 17,
        "nombre": "Huevos Revueltos con Champiñones",
        "descripcion": "Desayuno rápido y nutritivo con champiñones",
        "tiempo_preparacion": 15,
        "calorias": 260,
        "imagen_url": "/static/img/huevos-champinones.jpg",
        "tipo_comida": "desayuno",
        "ingredientes": [
            {"nombre": "Huevos", "cantidad": 2, "unidad": "unidades", "producto_id": 12, "precio": 0.50},
            {"nombre": "Champiñones", "cantidad": 100, "unidad": "g", "producto_id": 45, "precio": 1.00},
            {"nombre": "Aceite de oliva", "cantidad": 1, "unidad": "cucharada", "producto_id": 4, "precio": 0.10}
        ],
        "pasos": [
            "Limpiar y cortar los champiñones",
            "Saltearlos en aceite de oliva",
            "Añadir los huevos batidos y remover",
            "Cocinar hasta que estén al punto"
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
async def agregar_a_carrito(recetas_ids: List[int]):
    """
    Convierte las recetas seleccionadas en items del carrito
    Consolida ingredientes duplicados
    """
    try:
        carrito = {}
        
        # Consolidar ingredientes de todas las recetas
        for receta_id in recetas_ids:
            receta = next((r for r in RECETAS_EJEMPLO if r["id"] == receta_id), None)
            if not receta:
                continue
            
            for ing in receta["ingredientes"]:
                key = f"{ing['producto_id']}"
                
                if key in carrito:
                    carrito[key]["cantidad"] += ing["cantidad"]
                    carrito[key]["precio"] += ing["precio"]
                else:
                    carrito[key] = {
                        "producto_id": ing["producto_id"],
                        "nombre": ing["nombre"],
                        "cantidad": ing["cantidad"],
                        "unidad": ing["unidad"],
                        "precio": ing["precio"],
                        "recetas": [receta_id]
                    }
        
        items_carrito = list(carrito.values())
        total = sum(item["precio"] for item in items_carrito)
        
        return {
            "success": True,
            "carrito": {
                "items": items_carrito,
                "total": round(total, 2),
                "num_items": len(items_carrito)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

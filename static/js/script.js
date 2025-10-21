// ==================== ESTADO DE LA APLICACIÓN ====================
const appState = {
  menuActual: null,
  preferencias: null,
  carrito: [],
  recetaActual: null
};

// ==================== ELEMENTOS DEL DOM ====================
const elements = {
  // Botones principales
  btnEmpezar: document.getElementById('btnEmpezar'),
  btnCarrito: document.getElementById('btnCarrito'),
  cartBadge: document.getElementById('cartBadge'),
  
  // Modales
  modalPreferencias: document.getElementById('modalPreferencias'),
  modalReceta: document.getElementById('modalReceta'),
  btnCerrarModal: document.getElementById('btnCerrarModal'),
  btnCerrarReceta: document.getElementById('btnCerrarReceta'),
  
  // Formulario
  formPreferencias: document.getElementById('formPreferencias'),
  
  // Sección de menú
  menuSection: document.getElementById('menuSection'),
  menuGrid: document.getElementById('menuGrid'),
  costoTotal: document.getElementById('costoTotal'),
  btnRegenerarTodo: document.getElementById('btnRegenerarTodo'),
  btnConfirmarMenu: document.getElementById('btnConfirmarMenu'),
  
  // Detalle de receta
  recetaTitulo: document.getElementById('recetaTitulo'),
  recetaDetalle: document.getElementById('recetaDetalle')
};

// ==================== FUNCIONES DE API ====================

async function generarMenu(preferencias) {
  try {
    const response = await fetch('/api/generar-menu', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preferencias)
    });
    
    if (!response.ok) {
      throw new Error('Error al generar el menú');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    alert('Hubo un error al generar el menú. Por favor, intenta de nuevo.');
    return null;
  }
}

async function regenerarReceta(dia, preferencias) {
  try {
    const response = await fetch('/api/regenerar-receta', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ dia, preferencias })
    });
    
    if (!response.ok) {
      throw new Error('Error al regenerar la receta');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    alert('Hubo un error al regenerar la receta.');
    return null;
  }
}

async function agregarACarrito(recetasIds) {
  try {
    const response = await fetch('/api/agregar-a-carrito', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ recetas_ids: recetasIds })
    });
    
    if (!response.ok) {
      throw new Error('Error al agregar al carrito');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    alert('Hubo un error al agregar los ingredientes al carrito.');
    return null;
  }
}

// ==================== FUNCIONES DE UI ====================

function mostrarModal(modal) {
  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function cerrarModal(modal) {
  modal.classList.remove('active');
  document.body.style.overflow = 'auto';
}

function mostrarMenu(menuData) {
  appState.menuActual = menuData;
  
  // Mostrar sección de menú
  elements.menuSection.classList.remove('hidden');
  
  // Actualizar costo total
  elements.costoTotal.textContent = `€${menuData.costo_total.toFixed(2)}`;
  
  // Renderizar recetas
  elements.menuGrid.innerHTML = '';
  
  menuData.recetas.forEach((receta, index) => {
    const card = crearTarjetaReceta(receta, index + 1);
    elements.menuGrid.appendChild(card);
  });
  
  // Scroll suave a la sección de menú
  elements.menuSection.scrollIntoView({ behavior: 'smooth' });
}

function crearTarjetaReceta(receta, dia) {
  const card = document.createElement('div');
  card.className = 'recipe-card';
  
  const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
  const nombreDia = dias[dia - 1] || `Día ${dia}`;
  
  // Calcular costo de la receta
  const costoReceta = receta.ingredientes.reduce((total, ing) => total + ing.precio, 0);
  
  card.innerHTML = `
    <div class="recipe-image">
      🍽️
    </div>
    <div class="recipe-content">
      <span class="recipe-day">${nombreDia}</span>
      <h3>${receta.nombre}</h3>
      <p>${receta.descripcion}</p>
      <div class="recipe-meta">
        <span>⏱️ ${receta.tiempo_preparacion} min</span>
        <span>🔥 ${receta.calorias} kcal</span>
        <span>💰 €${costoReceta.toFixed(2)}</span>
      </div>
      <div class="recipe-actions">
        <button class="btn-view" onclick="verDetalleReceta(${receta.id})">
          👁️ Ver receta
        </button>
        <button class="btn-regenerate" onclick="regenerarRecetaIndividual(${dia})">
          🔄 Cambiar
        </button>
      </div>
    </div>
  `;
  
  return card;
}

function mostrarDetalleReceta(receta) {
  appState.recetaActual = receta;
  
  elements.recetaTitulo.textContent = receta.nombre;
  
  // Renderizar ingredientes
  const ingredientesHTML = `
    <div class="ingredients-section">
      <h4>📝 Ingredientes</h4>
      <ul class="ingredients-list">
        ${receta.ingredientes.map(ing => `
          <li>
            <span>${ing.nombre}</span>
            <span><strong>${ing.cantidad} ${ing.unidad}</strong></span>
          </li>
        `).join('')}
      </ul>
    </div>
  `;
  
  // Renderizar pasos
  const pasosHTML = `
    <div class="steps-section">
      <h4>👨‍🍳 Preparación</h4>
      <ol class="steps-list">
        ${receta.pasos.map(paso => `<li>${paso}</li>`).join('')}
      </ol>
    </div>
  `;
  
  // Información adicional
  const infoHTML = `
    <div class="recipe-meta" style="margin-bottom: 1.5rem;">
      <span>⏱️ ${receta.tiempo_preparacion} minutos</span>
      <span>🔥 ${receta.calorias} calorías</span>
    </div>
  `;
  
  elements.recetaDetalle.innerHTML = infoHTML + ingredientesHTML + pasosHTML;
  
  mostrarModal(elements.modalReceta);
}

function actualizarBadgeCarrito(cantidad) {
  elements.cartBadge.textContent = cantidad;
  
  if (cantidad > 0) {
    elements.cartBadge.style.display = 'inline-block';
  } else {
    elements.cartBadge.style.display = 'none';
  }
}

// ==================== FUNCIONES GLOBALES (llamadas desde HTML) ====================

window.verDetalleReceta = async function(recetaId) {
  try {
    const response = await fetch(`/api/receta/${recetaId}`);
    const data = await response.json();
    
    if (data.success) {
      mostrarDetalleReceta(data.receta);
    }
  } catch (error) {
    console.error('Error al obtener receta:', error);
  }
};

window.regenerarRecetaIndividual = async function(dia) {
  if (!appState.preferencias) return;
  
  const btnRegenerar = event.target;
  btnRegenerar.disabled = true;
  btnRegenerar.textContent = '⏳ Generando...';
  
  const resultado = await regenerarReceta(dia, appState.preferencias);
  
  if (resultado && resultado.success) {
    // Actualizar la receta en el estado
    const index = dia - 1;
    appState.menuActual.recetas[index] = resultado.receta;
    
    // Re-renderizar el menú
    mostrarMenu(appState.menuActual);
  }
  
  btnRegenerar.disabled = false;
  btnRegenerar.textContent = '🔄 Cambiar';
};

// ==================== EVENT LISTENERS ====================

// Abrir modal de preferencias
elements.btnEmpezar.addEventListener('click', () => {
  mostrarModal(elements.modalPreferencias);
});

// Cerrar modales
elements.btnCerrarModal.addEventListener('click', () => {
  cerrarModal(elements.modalPreferencias);
});

elements.btnCerrarReceta.addEventListener('click', () => {
  cerrarModal(elements.modalReceta);
});

// Cerrar modal al hacer clic fuera
elements.modalPreferencias.addEventListener('click', (e) => {
  if (e.target === elements.modalPreferencias) {
    cerrarModal(elements.modalPreferencias);
  }
});

elements.modalReceta.addEventListener('click', (e) => {
  if (e.target === elements.modalReceta) {
    cerrarModal(elements.modalReceta);
  }
});

// Submit del formulario de preferencias
elements.formPreferencias.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // Recoger datos del formulario
  const formData = new FormData(e.target);
  const preferencias = {
    objetivo: formData.get('objetivo'),
    tiempo_cocina: formData.get('tiempo_cocina'),
    alergias: [],
    num_personas: parseInt(formData.get('num_personas')),
    presupuesto: parseFloat(formData.get('presupuesto')),
    estilo_cocina: formData.get('estilo_cocina'),
    preferencia_marca: formData.get('preferencia_marca')
  };
  
  appState.preferencias = preferencias;
  
  // Cerrar modal
  cerrarModal(elements.modalPreferencias);
  
  // Mostrar loader (opcional)
  elements.menuGrid.innerHTML = '<p style="text-align: center; padding: 2rem;">⏳ Generando tu menú personalizado...</p>';
  elements.menuSection.classList.remove('hidden');
  
  // Generar menú
  const resultado = await generarMenu(preferencias);
  
  if (resultado && resultado.success) {
    mostrarMenu(resultado.menu);
  }
});

// Regenerar todo el menú
elements.btnRegenerarTodo.addEventListener('click', async () => {
  if (!appState.preferencias) return;
  
  elements.btnRegenerarTodo.disabled = true;
  elements.btnRegenerarTodo.textContent = '⏳ Regenerando...';
  
  const resultado = await generarMenu(appState.preferencias);
  
  if (resultado && resultado.success) {
    mostrarMenu(resultado.menu);
  }
  
  elements.btnRegenerarTodo.disabled = false;
  elements.btnRegenerarTodo.textContent = '🔄 Regenerar todo el menú';
});

// Confirmar y añadir al carrito
elements.btnConfirmarMenu.addEventListener('click', async () => {
  if (!appState.menuActual) return;
  
  elements.btnConfirmarMenu.disabled = true;
  elements.btnConfirmarMenu.textContent = '⏳ Añadiendo al carrito...';
  
  const recetasIds = appState.menuActual.recetas.map(r => r.id);
  const resultado = await agregarACarrito(recetasIds);
  
  if (resultado && resultado.success) {
    appState.carrito = resultado.carrito.items;
    actualizarBadgeCarrito(resultado.carrito.num_items);
    
    alert(`✅ ¡Genial! Se han añadido ${resultado.carrito.num_items} productos al carrito por un total de €${resultado.carrito.total.toFixed(2)}`);
  }
  
  elements.btnConfirmarMenu.disabled = false;
  elements.btnConfirmarMenu.textContent = '✅ Confirmar y añadir al carrito';
});

// Ver carrito
elements.btnCarrito.addEventListener('click', () => {
  if (appState.carrito.length === 0) {
    alert('Tu carrito está vacío. Primero genera un menú y confírmalo.');
    return;
  }
  
  // En producción, esto redirigiría a la página del carrito
  alert(`Carrito: ${appState.carrito.length} productos`);
  console.log('Contenido del carrito:', appState.carrito);
});

// ==================== INICIALIZACIÓN ====================
console.log('✅ SupermercAI cargado correctamente');
console.log('🚀 Versión: 1.0.0');

const API_URL = "/tasks";

const lista = document.getElementById("lista-tareas");
const botonesFiltro = document.querySelectorAll(".filtro");
const botonCrear = document.getElementById("btn-crear");

let filtroActual = "todas";

botonCrear.addEventListener("click", () => {
  window.location.href = "formulario.html";
});

botonesFiltro.forEach(boton => {
  boton.addEventListener("click", () => {
    botonesFiltro.forEach(b => b.classList.remove("activo"));
    boton.classList.add("activo");
    filtroActual = boton.dataset.filtro;
    cargarTareas();
  });
});

async function cargarTareas() {
  try {
    const respuesta = await fetch(API_URL);
    const tareas = await respuesta.json();

    const tareasFiltradas = tareas.filter(t => {
      if (filtroActual === "pendientes") return !t.completed;
      if (filtroActual === "completadas") return t.completed;
      return true;
    });

    lista.innerHTML = "";
    if (tareasFiltradas.length === 0) {
      lista.innerHTML = `
        <li class="lista-vacia">
          <p>No tienes tareas todavía</p>
        </li>
      `;
      document.getElementById("btn-crear-vacio").addEventListener("click", () => {
        window.location.href = "formulario.html";
      });
      return;
    }
    tareasFiltradas.forEach(tarea => {
      const li = document.createElement("li");
      li.className = tarea.completed ? "tarea completada" : "tarea";
      li.innerHTML = `
        <div class="tarea-contenido">
          <span class="tarea-titulo">${tarea.title}</span>
          ${tarea.description ? `<p class="tarea-descripcion">${tarea.description}</p>` : ""}
        </div>
        <div class="tarea-acciones">
          <button class="btn-completar">✔</button>
          <button class="btn-editar">✎</button>
          <button class="btn-eliminar">🗑</button>
        </div>
      `;

      li.querySelector(".btn-completar").addEventListener("click", () => {
        completarTarea(tarea);
      });

      li.querySelector(".btn-editar").addEventListener("click", () => {
        window.location.href = `formulario.html?id=${tarea.id}`;
      });

      li.querySelector(".btn-eliminar").addEventListener("click", () => {
        eliminarTarea(tarea.id);
      });

      lista.appendChild(li);
    });
  } catch (error) {
    console.error("Error al cargar tareas:", error);
  }
}

async function completarTarea(tarea) {
  try {
    await fetch(`${API_URL}/${tarea.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...tarea, completed: !tarea.completed })
    });
    cargarTareas();
  } catch (error) {
    console.error("Error al actualizar tarea:", error);
  }
}

async function eliminarTarea(id) {
  try {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    cargarTareas();
  } catch (error) {
    console.error("Error al eliminar tarea:", error);
  }
}

cargarTareas();
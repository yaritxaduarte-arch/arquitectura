const API_URL = "/tasks";

const form = document.getElementById("form-tarea");
const inputTitle = document.getElementById("title");
const inputDescription = document.getElementById("description");
const tituloPagina = document.getElementById("titulo-pagina");
const btnCancelar = document.getElementById("btn-cancelar");

const params = new URLSearchParams(window.location.search);
const taskId = params.get("id");

if (taskId) {
  tituloPagina.textContent = "Editar tarea";
  cargarTarea(taskId);
}

btnCancelar.addEventListener("click", () => {
  window.location.href = "index.html";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const datos = {
    title: inputTitle.value,
    description: inputDescription.value
  };

  try {
    let respuesta;
    if (taskId) {
      respuesta = await fetch(`${API_URL}/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
      });
    } else {
      respuesta = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
      });
    }

    if (!respuesta.ok) {
      const error = await respuesta.json();
      alert(error.detail);
      return;
    }

    window.location.href = "index.html";
  } catch (error) {
    console.error("Error al guardar la tarea:", error);
  }
});

async function cargarTarea(id) {
  try {
    const respuesta = await fetch(`${API_URL}/${id}`);
    const tarea = await respuesta.json();
    inputTitle.value = tarea.title;
    inputDescription.value = tarea.description || "";
  } catch (error) {
    console.error("Error al cargar la tarea:", error);
  }
}
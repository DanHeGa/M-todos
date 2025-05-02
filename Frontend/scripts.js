async function getData() {
    try {
      const response = await fetch('http://localhost:2000/api/registros/generales');
      if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
      const data = await response.json();
      document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      document.getElementById("output").textContent = "❌ Error al obtener datos: " + err.message;
    }
  }
  
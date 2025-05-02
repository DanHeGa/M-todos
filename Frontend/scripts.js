async function getData() {
  try {
    const alfabeto = document.getElementById("alfabeto").value;
    const regex = document.getElementById("ER").value;

    const response = await fetch('/convertor', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ regex, alfabeto })
    });

    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
    const data = await response.json();

    document.getElementById("output").innerHTML = data.svg; // Mostrar SVG
  } catch (err) {
    document.getElementById("output").textContent = "Error: " + err.message;
  }
}

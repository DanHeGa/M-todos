let currentRegex = ""; //

async function getData() {
  try {
    const alfabeto = document.getElementById("alfabeto").value;
    const regex = document.getElementById("ER").value;

    currentRegex = regex;

    const response = await fetch('/convertor', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ regex, alfabeto })
    });

    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
    const data = await response.json();

    document.getElementById("output").innerHTML = data.svg; // Mostrar SVG
    currentDfa = data.dfa;
    document.getElementById("wordCheck").style.display = "block";
  } catch (err) {
    document.getElementById("output").textContent = "Error: " + err.message;
  }
}

async function checkWord() {
  try {
    const word = document.getElementById("inputWord").value;
    const response = await fetch('/wordChecker', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `Error HTTP: ${response.status}`);
    }
    
    const data = await response.json();
    document.getElementById("output2").innerHTML = data.inLanguage
      ? "La palabra pertenece al lenguaje"
      : "La palabra NO pertenece al lenguaje";
  } catch(error) {
    document.getElementById("output2").innerHTML = "Error: " + error.message;
  }
}
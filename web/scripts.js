document.getElementById("city").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        // Tutaj możesz umieścić kod, który ma się wykonać po wciśnięciu Enter
        alert("Wcisnąłeś Enter po wpisaniu tekstu: " + this.value);
    }
});
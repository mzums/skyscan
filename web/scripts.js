//document.getElementById('city').value = ''
document.getElementById("city").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        fetch('http://api.openweathermap.org/data/2.5/weather?q='+this.value+'&units=metric&appid=e1e260bb69ce72bf8562cebe1feb4ee3')
        .then(response => {
            if (!response.ok) {
                throw new Error("HTTP error, status: " + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log(data['weather'][0]['description']);
            var output = document.getElementById("output");
            output.innerHTML = this.value + "<br>" + data['weather'][0]['description'];
        })
        .catch(err => {
            //console.error(err);
            alert("Error downloading weather data!");
        });
    }
});

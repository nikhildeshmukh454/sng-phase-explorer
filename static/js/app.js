function showLoading(){

const screen = document.getElementById("loading-screen");

screen.style.display = "flex";

}


/* Button animation */

document.addEventListener("DOMContentLoaded", function(){

const btn = document.querySelector(".btn");

if(btn){

btn.addEventListener("click", function(){

btn.innerHTML = "Calculating...";
btn.style.opacity = "0.7";

});

}

});


function updateVal(id){
document.getElementById(id+"_val").innerText =
document.getElementById(id).value
}

function generatePlot(){

let comp = [
N2.value,
CO2.value,
C1.value,
C2.value,
C3.value,
IC4.value,
NC4.value,
IC5.value,
NC5.value,
NC6.value,
NC7.value,
NC8.value,
NC10.value
]

fetch("/custom",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
composition:comp
})

})

.then(res=>res.json())
.then(data=>{
document.getElementById("plot").src = data.plot + "?t=" + new Date().getTime()
})

}
const collapsee = document.getElementById("collapse")
collapsee.addEventListener('click', function(e){
    e.preventDefault();
    document.body.classList.toggle('sb-expanded');
});


submit = document.getElementById("find");

function result(){
    working = Number(document.getElementById("working").value);
    present = Number(document.getElementById("present").value);
    percentage = present/working * 100; 
    message = document.getElementById("message");
    percentage_field = document.getElementById("number");

    if (percentage >= 80){
    message.textContent = "ITS OVER 80!";
    message.style.color = "green";
    percentage_field.style.color = "green";
    percentage_field.textContent = percentage.toFixed(2) + "%";
    
    } else if (percentage < 80){
        message.textContent = "Not Enough!"
        message.style.color = "red";
        percentage_field.style.color = "red";
        percentage_field.textContent = percentage.toFixed(2) + "%";

    } else{
        message.textContent = "Insufficient Value";
        message.style.color = "yellow";
    }
    document.getElementById("working_hidden").value = Number(working);
    document.getElementById("present_hidden").value = Number(present);
    document.getElementById("percentage_hidden").value = percentage;
}

function syncdata(){
    result()
}


let endpoint = "http://localhost:2808/api/v1/";
let type = "";

get_data = function(){
    id = document.getElementById("add_box").value;
    type = document.getElementById("type").innerHTML;
    add_media(id, type);
}

var add_media = function(id, type) {
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    xmlhttp.open("POST", endpoint + "add_media");
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({"media_type": type, "media_id": id.replace(/\D/g,'')}));
    xmlhttp.onload  = function() {
        var jsonResponse = JSON.parse(xmlhttp.responseText);
        alert(jsonResponse.title + " added to your list!");
        choose();
        }
     };


var set_type = function(type) {
    const type_ = document.createElement("span");
    type_.id = "type";
    type_.innerText = type;
    type_.style.display = "none";
    document.body.appendChild(type_);

    document.getElementById("choose").style.display = "none";
    document.getElementById("adding").style.display = "flex";
    document.getElementById("add_box").setAttribute("placeholder", "Enter " + type + " ID");
    
}

var choose = function() {
    document.getElementById("adding").style.display = "none";
    document.getElementById("choose").style.display = "flex";
}

function init () {
    choose();
}

window.onload = init;

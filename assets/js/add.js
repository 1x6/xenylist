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

var search = function() {
    query = document.getElementById("search_box").value;
    $.getJSON(endpoint + "search?query=" + query, function(results) {
        document.getElementById("search-box").style = "transform: translate(-50%, -350%);"
        document.getElementById("results-container").style = "display: flex;"
        results["data"]["anime"]["results"].forEach(data => {
            add_result(data, "anime");
        });
        results["data"]["manga"]["results"].forEach(data => {
            add_result(data, "manga");
        });
    });
};
    
var add_result = function(data, type) {
    const node = document.createElement("div");
    node.className = "result";
    const h2 = document.createElement("h2");
    h2.innerHTML = data["title"]["english"] != null ? data["title"]["english"] : data["title"]["romaji"];
    node.appendChild(h2);
    const h3 = document.createElement("h3");
    h3.innerHTML = data["startDate"]["year"] + " " + data["format"];
    node.appendChild(h3);
    document.getElementById("results-" + type).appendChild(node);
}

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
    // choose();
}

window.onload = init;

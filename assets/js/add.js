let endpoint = "http://localhost:2808/api/v1/";
// let endpoint = "http://192.168.1.52:2808/api/v1/";
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

function load_more() {
    if (localStorage.getItem("load_more_last") > 0) {
        page = localStorage.getItem("load_more_last");
        clear_results();
        search(page);
    } else {
        localStorage.setItem("load_more_last", 0);
        search(0);
    };
};

function search(page) {
    var p2 = parseInt(page) + 2;
    query = document.getElementById("search_box").value;
    $.getJSON(endpoint + "search?query=" + query, function(results) {
        document.getElementById("search-box").style = "transform: translate(-50%, -350%);"
        clear_results();
        document.getElementById("results-container").style = "display: flex;"
        all_anime = [];
        all_manga = [];
        results["data"]["anime"]["results"].forEach(data => {
            all_anime.push(data);
        });
        results["data"]["manga"]["results"].forEach(data => {
            all_manga.push(data);
        });
        add_result(all_anime.slice(page, p2));
        add_result(all_manga.slice(page, p2));
        localStorage.setItem("load_more_last", p2);
    
    });
}

    
var add_result = function(data) {

    for (let i = 0; i < data.length; i++) {
        console.log(data[i])
        var node = document.createElement("div"); 
        node.className = "result";
        const title = data[i]["title"]["english"] != null ? data[i]["title"]["english"] : data[i]["title"]["romaji"]
        node.setAttribute("onclick", `ask_confirm('${title}', '${data[i]["id"]}', '${data[i]["type"].toLowerCase()}');`)
        const h2 = document.createElement("h2");
        h2.innerHTML = elipsis(title, 40);
        node.appendChild(h2);
        const h3 = document.createElement("h3");
        h3.innerHTML = data[i]["startDate"]["year"] + " " + data[i]["format"];
        node.appendChild(h3);
        //document.getElementById("results-" + type).appendChild(node);
        document.getElementById("results").appendChild(node);
    }
    
}



var clear_results = function() {
    for(let element of document.getElementsByClassName("results-container")) {
        element.innerHTML = "";
    }
}

var ask_confirm = function(title, id, type) {
    if(confirm("Do you want to add " + title + " to your list?")) {
        add_media(id, type);
    }
}

function elipsis(string, max_length) {
    if (string.length > max_length) {
      return string.slice(0, max_length) + "..";
    } else {
      return string;
    }
  }
  
// manual entry, unused

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

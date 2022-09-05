let endpoint = "http://localhost:2808/api/v1/";

function load_more() {
    if (localStorage.getItem("load_more_page") > 0) {
        page = localStorage.getItem("load_more_page");
        clear_results();
        //search(page);
        display_results(page);
    };

    if (all_anime.length + all_manga.length == 0) {
        document.getElementById("load_more").style.display = "none";
    } else {
        document.getElementById("load_more").style.display = "";
    }
};

function display_results(page) {

    if (max_len < 4) {
        document.getElementById("load_more").style.display = "none";
    }

    page = parseInt(page);
    console.log(max_len)
    
    console.log(max_len)
    document.getElementById("search-box").style = "transform: translate(-50%, -350%);"
    
    document.getElementById("results-container").style = "display: flex;"

    add_result(all_anime.splice(0, 2));

    var node = document.createElement("hr");
    node.style = "width: 50%;";
    node.setAttribute("id", "line");
    document.getElementById("results").appendChild(node);

    add_result(all_manga.splice(0, 2));

    localStorage.setItem("load_more_page", page + 1);

    if (all_anime.length == 0 || all_manga.length == 0) {
        document.getElementById("line").remove();
    }

}

function search() {
    clear_results();

    query = document.getElementById("search_box").value;
    $.getJSON(endpoint + "search?query=" + query, function(results) {
        
        all_anime = [];
        all_manga = [];
        
        results["data"]["anime"]["results"].forEach(data => {
            all_anime.push(data);
        });
        results["data"]["manga"]["results"].forEach(data => {
            all_manga.push(data);
        });

        max_len = all_anime.length + all_manga.length;
        
        //localStorage.setItem("all_anime", all_anime);
        //localStorage.setItem("all_manga", all_manga);
        localStorage.setItem("load_more_page", 1);

        display_results(1);
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
  
function isOdd(num) {
    if ((num % 2) == 1) {
        return true;
    } else {
        return false;
    }
}
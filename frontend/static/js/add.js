const loc = window.location.href;
const endpoint = `${loc.split("://")[0]}://${loc.split("/")[2]}/api/`;

let all_anime = [];
let all_manga = [];
let max_len = 0;

function loadMore() {
    const page = localStorage.getItem("load_more_page");
    if (page > 0) {
        clearResults();
        displayResults(page);
    }

    if (all_anime.length + all_manga.length < 1) {
        document.getElementById("load_more").style.display = "none";
    } else {
        document.getElementById("load_more").style.display = "";
    }
}

function displayResults(page) {
    const an = all_anime.length;
    const ma = all_manga.length;
    const loadMoreButton = document.getElementById("load_more");

    if (!loadMoreButton) {
        const node = document.createElement("button");
        node.setAttribute("id", "load_more");
        node.setAttribute("onclick", "loadMore();");
        node.setAttribute("class", "load-more");
        node.innerHTML = "Load more";
        document.getElementById("results").appendChild(node);
    }

    if (max_len < 4) {
        document.getElementById("load_more").style.display = "none";
    } else {
        document.getElementById("load_more").style.display = "";
    }

    page = parseInt(page);

    document.getElementById("search-box").style = "transform: translate(-50%, -250%);"

    document.getElementById("results-container").style = "display: flex;";

    addResult(all_anime.splice(0, 2));

    const hr = document.createElement("hr");
    hr.style = "width: 100%;";
    hr.setAttribute("id", "line");
    document.getElementById("results").appendChild(hr);

    addResult(all_manga.splice(0, 2));

    if (an === 0 || ma === 0) {
        document.getElementById("line").remove();
    }

    document.getElementById("results").appendChild(document.getElementById("load_more"));

    localStorage.setItem("load_more_page", page + 1);
}

function search() {
    clearResults();

    const query = document.getElementById("search_box").value;
    $.getJSON(`${endpoint}search?query=${query}`, function(results) {
        all_anime = results.data.anime.results;
        all_manga = results.data.manga.results;

        max_len = all_anime.length + all_manga.length;

        localStorage.setItem("load_more_page", 1);

        displayResults(1);
    });
}

function addResult(data) {
    for (let i = 0; i < data.length; i++) {
        const node = document.createElement("div"); 
        node.classList.add("result");

        const title = data[i]["title"]["english"] ? data[i]["title"]["english"] : data[i]["title"]["romaji"]
        const id = data[i]["id"];
        const type = data[i]["type"].toLowerCase();
        node.addEventListener("click", () => askConfirm(title, id, type));

        const h2 = document.createElement("h2");
        h2.style = "z-index: 1; position: inherit;"
        h2.innerHTML = elipsis(title, 40);
        node.appendChild(h2);

        const h3 = document.createElement("h3");
        h3.style = "z-index: 1; position: inherit;"
        h3.innerHTML = data[i]["startDate"]["year"] + " " + data[i]["format"];
        node.appendChild(h3);

        const img = document.createElement("div");
        img.style.backgroundImage = `url(${data[i]["coverImage"]["medium"]})`;
        img.classList.add("result-bg");
        node.appendChild(img);

        document.getElementById("results").appendChild(node);
    }
}

function addMedia(id, type) {
    const payload = {media_type: type, media_id: id.replace(/\D/g,'')};
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify(payload)
    };

    fetch(endpoint + 'add_media', options)
        .then(response => response.json())
        .then(json => {
            alert(`${json.title} added to your list!`);
            location.reload();
        });
}

function askConfirm(title, id, type) {
    if(confirm(`Do you want to add ${title} to your list?`)) {
        addMedia(id, type);
    }
}

function clearResults() {
    const resultsElements = document.getElementsByClassName("results-container");
    for(const element of resultsElements) {
        element.innerHTML = "";
    }
}

function elipsis(string, maxLength) {
    if (string.length > maxLength) {
        return string.slice(0, maxLength) + "..";
    } else {
        return string;
    }
}

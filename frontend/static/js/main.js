var loc = window.location.href
let endpoint = loc.split("://")[0] + "://" + loc.split("/")[2] + "/api/"
console.log("detected host: ", endpoint)


if (document.location.href.includes("anime")) {
  var type = "anime";
} 
if (document.location.href.includes("manga")) {
  var type = "manga";
} 

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

/* credit to w3schools for this */
function search() {
  var input, filter, table, tr, td, i, txtValue;
  var input = document.getElementById("search");
  var filter = input.value.toUpperCase();
  var table = document.getElementById("mediaTable");
  var tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}
/* /////////////////////////// */

var delete_entry = function(id) {
  var r = confirm("Are you sure you want to delete this entry?");
  if (r == true) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", endpoint + "delete");
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({"media_type": type, "media_id": id}));
    // get xmlhttp response code
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        location.reload();
      }
    }
  }
};


var get_rating_type = function() {
  $.getJSON(endpoint + "rating_type", function(resp, status){
  
      console.log(resp);
      if (resp.rating_type == "stars") {
        rating_type = "stars";
      } else {
        rating_type = "ten";
      }
    })
  
  get_list();
    
}

var edit_mode = function(row_id) {
  var status_cell = document.getElementById("status-" + row_id);
  let actual_status = status_cell.innerHTML;
  var row = document.getElementById(row_id);
  var status = row.cells[2];
  var prog = row.cells[3];
  var score = row.cells[4];
  var edit_btn = row.cells[5];
  row.insertCell(6).innerHTML = "<i onclick='delete_entry(" + row_id + ")' class='fa-solid fa-trash'></i>";
  var delete_btn = row.cells[6];
  status.outerHTML = 
          `<td> 
            <select id='status-` + row_id + `'> 
              <option value='current'>Current</option>
              <option value='planning'>Planning</option>
              <option value='completed'>Completed</option>
              <option value='paused'>Paused</option>
              <option value='dropped'>Dropped</option>
            </select> </td>`;
    var options = document.getElementById("status-" + row_id).options;
    for (var i1 = 0; i1 < options.length; i1++) {
      if (options[i1].value == actual_status) {
      options[i1].selected = true;
      break;
      }
    }
  prog.setAttribute("contenteditable", "true");
  score.setAttribute("contenteditable", "true");
  edit_btn.innerHTML = "<i onclick='done_edit(" + row_id + ")' class='fa-solid fa-check'></i>";
}

var done_edit = function(row_id) {
  var status_cell = document.getElementById("status-" + row_id);
  status_fr = status_cell.value;
  row = document.getElementById(row_id);
  var status = row.cells[2]
  var prog = row.cells[3];
  var score = row.cells[4];
  var edit_btn = row.cells[5];
  var delete_btn = row.cells[6];
  prog.setAttribute("contenteditable", "false");
  score.setAttribute("contenteditable", "false");
  status.outerHTML = "<td class='status' id='status-" + row_id + "'>" + capitalizeFirstLetter(status_fr) +"</td>";
  edit_btn.innerHTML = "<i onclick='edit_mode(" + row_id + ")' class='fa-solid fa-pencil'></i>";
  delete_btn.remove();
  update_entry(row_id, prog.innerHTML.replace(/\D/g, ""), score.innerHTML.replace(/\D/g, ""), status_fr);
}

var update_entry = function(id, progress, score, status) {
  var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
  xmlhttp.open("POST", endpoint + "edit");
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlhttp.send(JSON.stringify({"media_type": type, "media_id": id, "progress": progress, "score": score, "status": status}));
}

var filter_buttons = function() {
  document.getElementById("current").onclick = function() {hide_except("current")};
  document.getElementById("completed").onclick = function() {hide_except("completed")};
  document.getElementById("paused").onclick = function() {hide_except("paused")};
  document.getElementById("dropped").onclick = function() {hide_except("dropped")};
  document.getElementById("planning").onclick = function() {hide_except("planning")};
  document.getElementById("all").onclick = function() {hide_except("all")};
}
     
var hide_except = function(type) {
  var table = document.getElementById("mediaTable");
  var rows = table.rows;
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].id !== "headers") {
      if (type == "all") {
        rows[i].style.display = "";
      }
      else {
      if (rows[i].className !== type) {
        rows[i].style.display = "none";
      } else {
        rows[i].style.display = "";
      }
  }
  }
}
};

var show_count = function(type) {
  var table = document.getElementById("mediaTable");
  var rows = table.rows;
  var elem = document.getElementById(type);
  
  
  if (type === "all") {
    elem.innerHTML = `${capitalizeFirstLetter(type)} (${(rows.length - 1).toString()})`
  } else {
    var count = 0;
    for (var i = 0; i < rows.length; i++) {
      if (rows[i].id !== "headers") {
        if (rows[i].className == type) {
          count++;
        }
      }
    }
    elem.innerHTML = `${capitalizeFirstLetter(type)} (${(count).toString()})` //elem.innerHTML + (count).toString()
  }
}
    

function render_table(resp, table) {
  for (let i = 0; i < resp.length; i++) {

    var row = table.insertRow(i+1);
    row.id = resp[i].media_id;
    row.className = resp[i].status.toLowerCase(); 
    //var type = resp[i].media_type; do this maybe
    
    var link = "https://anilist.co/" + type + "/" + resp[i].media_id
    var _img = row.insertCell(0).innerHTML = "<img class='cover-icon' id='" + row.id + "'src='" + resp[i].image + "'>";
    var title = row.insertCell(1).outerHTML = "<td class='title' id='title-" + row.id + "'>" + resp[i].title + "</td>";
    document.getElementById("title-" + row.id).setAttribute("onclick", "window.open('" + link + "')");
    document.getElementById("title-" + row.id).setAttribute("style", "cursor: pointer");
    var status = row.insertCell(2).outerHTML = "<td id='status-" + row.id + "'>" + capitalizeFirstLetter(resp[i].status) + "</td>";
    var prog = row.insertCell(3).outerHTML = "<td class='center' id='progress-" + row.id + "'>" + resp[i].progress + "</td>";
    if (rating_type === "stars") {
      var score = row.insertCell(4).outerHTML = `<td class='center' id='score-${row.id}'>${resp[i].score} <i class='fa-solid fa-star'></i></td>`;
    } else {
      var score = row.insertCell(4).outerHTML = `<td class='center' id='score-${row.id}'>${resp[i].score}</td>`;
    }
    var edit_btn = row.insertCell(5);
    edit_btn.innerHTML = "<i onclick='edit_mode(" + row.id + ")' class='fa-solid fa-pencil'></i>";
  }
}


var get_list = function() {
    
  $.getJSON(endpoint + "list/" + type, function(resp, status){
      //alert("Data: " + resp + "\nStatus: " + status);
      var table = document.getElementById("mediaTable");

      headers = table.insertRow(0);
      headers.id = "headers";
      headers.insertCell(0);
      headers.insertCell(1).outerHTML = "<th align='left'>Title</th>";
      headers.insertCell(2).outerHTML = "<th align='left'>Status</th>";
      headers.insertCell(3).outerHTML = "<th>Progress</th>";
      headers.insertCell(4).outerHTML = "<th>Score</th>";

      ///////////////////////////////////
      render_table(resp, table);
      filter_buttons();
      hide_except("current");
      types = ["current", "completed", "paused", "dropped", "planning", "all"];
      for (let i = 0; i < types.length; i++) {
        show_count(types[i]);
      }
    });
  };
  
  // Get the new one.
window.addEventListener('load', function() {
  get_rating_type();
});


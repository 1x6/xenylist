let endpoint = "http://192.168.1.113:2808/api/v1/"

var edit_mode = function(row_id) {
  row = document.getElementById(row_id);
  var prog = row.cells[2];
  var score = row.cells[3];
  var edit_btn = row.cells[4];
  prog.setAttribute("contenteditable", "true");
  score.setAttribute("contenteditable", "true");
  edit_btn.innerHTML = "<i onclick='done_edit(" + row_id + ")' class='fa-solid fa-check'></i>";
}

var done_edit = function(row_id) {
  row = document.getElementById(row_id);
  var prog = row.cells[2];
  var score = row.cells[3];
  var edit_btn = row.cells[4];
  prog.setAttribute("contenteditable", "false");
  score.setAttribute("contenteditable", "false");
  edit_btn.innerHTML = "<i onclick='edit_mode(" + row_id + ")' class='fa-solid fa-pencil'></i>";
  update_entry(row_id, prog.innerHTML, score.innerHTML);
}

var update_entry = function(id, progress, score) {
  var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
  xmlhttp.open("POST", endpoint + "edit");
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlhttp.send(JSON.stringify({"media_type": "anime", "mediaId": id, "progress": progress, "score": score}));
}


var get_list = function() {
  //var type = document.getElementById("mediaType").value;
  // add media type shit

  var type = "anime";
  $.getJSON(endpoint + "list/anime", function(resp, status){
      //alert("Data: " + resp + "\nStatus: " + status);
      var table = document.getElementById("mediaTable");

      headers = table.insertRow(0);
      img = headers.insertCell(0);
      title = headers.insertCell(1).outerHTML = "<th>Title</th>";
      progress = headers.insertCell(2).outerHTML = "<th>Progress</th>";
      score = headers.insertCell(3).outerHTML = "<th>Score</th>";

      ///////////////////////////////////

        for (let i = 0; i < resp.length; i++) {
          row = table.insertRow(i+1);
          row.id = resp[i].mediaId;
          var link = "https://anilist.co/" + type + "/" + resp[i].mediaId
          var _img = row.insertCell(0).innerHTML = "<img class='cover-icon' id='" + i+1 + "'src='" + resp[i].media.coverImage.large + "'>";
          var title = row.insertCell(1).outerHTML = "<td id='title-" + i+1 + "'>" + resp[i].media.title.english + "</td>";
          document.getElementById("title-" + i+1).setAttribute("onclick", "window.open('" + link + "')");
          document.getElementById("title-" + i+1).setAttribute("style", "cursor: pointer");
          var prog = row.insertCell(2).outerHTML = "<td id='progress-" + i+1 + "'>" + resp[i].progress + "</td>";
          var score = row.insertCell(3).outerHTML = "<td id='score-" + i+1 + "'>" + resp[i].score + "</td>"; // get property with .name .progress .score on cars[i] which is json dict
          var edit_btn = row.insertCell(4);
          edit_btn.innerHTML = "<i onclick='edit_mode(" + row.id + ")' class='fa-solid fa-pencil'></i>";
          edit_btn.setAttribute("style", "cursor: pointer");
        }
    
    
    });
  };
  
  // Get the new one.
  get_list();
  // Start the countdown.
  //setInterval(getList, 1000);
  

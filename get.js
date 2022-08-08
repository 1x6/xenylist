var apiData = {
    baseURL:
      "http://192.168.1.113:2808/api/v1/watching",
    additional: "",
    type: "anime"
    //api_key: "6628d543d56243388312c0a24ad871e4",
  };
  
  var getList = function() {
    $.getJSON(apiData.baseURL, function(resp, status){
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
            var link = "https://anilist.co/" + apiData.type + "/" + resp[i].mediaId
            var aimg = row.insertCell(0).innerHTML = "<img class='cover-icon' src='" + resp[i].media.coverImage.large + "'>";
            var atitle = row.insertCell(1).outerHTML = "<td id='title-" + i+1 + "'>" + resp[i].media.title.english + "</td>";
            document.getElementById("title-" + i+1).setAttribute("onclick", "window.open('" + link + "')");
            document.getElementById("title-" + i+1).setAttribute("style", "cursor: pointer");
            var aprog = row.insertCell(2).innerHTML = resp[i].progress;
            var ascore = row.insertCell(3).innerHTML = resp[i].score; // get property with .name .progress .score on cars[i] which is json dict
              
          }
      
      
      });
  };
  
  // Get the new one.
  getList();
  // Start the countdown.
  //setInterval(getList, 1000);
  

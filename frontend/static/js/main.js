const endpoint = `${window.location.protocol}//${window.location.host}/api/`;
const type = document.location.href.includes("anime") ? "anime" : "manga";

const capitalizeFirstLetter = (string) =>
  string.charAt(0).toUpperCase() + string.slice(1);

const search = () => {
  const input = document.getElementById("search");
  const filter = input.value.toUpperCase();
  const table = document.getElementById("mediaTable");
  const tr = table.getElementsByTagName("tr");

  for (let i = 0; i < tr.length; i++) {
    const td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      const txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
};

const delete_entry = (id) => {
  const confirmDelete = confirm("Are you sure you want to delete this entry?");
  if (confirmDelete) {
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", endpoint + "delete");
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({ media_type: type, media_id: id }));
    xmlhttp.onreadystatechange = () => {
      if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
        location.reload();
      }
    };
  }
};

const get_rating_type = () => {
  $.getJSON(endpoint + "rating_type", (resp, status) => {
    if (resp.rating_type === "stars") {
      rating_type = "stars";
    } else {
      rating_type = "ten";
    }
    get_list();
  });
};

const edit_mode = (row_id) => {
  const status_cell = document.getElementById(`status-${row_id}`);
  const actual_status = status_cell.innerHTML;
  const row = document.getElementById(row_id);
  const [status, prog, score, edit_btn] = row.cells.slice(2);
  const delete_btn = row.insertCell(-1);
  delete_btn.innerHTML = `<i onclick='delete_entry(${row_id})' class='fa-solid fa-trash'></i>`;
  status.innerHTML = `
    <select id='status-${row_id}'>
      <option value='current'>Current</option>
      <option value='planning'>Planning</option>
      <option value='completed'>Completed</option>
      <option value='paused'>Paused</option>
      <option value='dropped'>Dropped</option>
    </select>`;
  const options = status.querySelector("select").options;
  for (const option of options) {
    if (option.value === actual_status) {
      option.selected = true;
      break;
    }
  }
  prog.setAttribute("contenteditable", "true");
  score.setAttribute("contenteditable", "true");
  edit_btn.innerHTML = `<i onclick='done_edit(${row_id})' class='fa-solid fa-check'></i>`;
};

const done_edit = (row_id) => {
  const status_cell = document.getElementById(`status-${row_id}`);
  const status_fr = status_cell.value;
  const row = document.getElementById(row_id);
  const [status, prog, score, edit_btn, delete_btn] = row.cells;
  prog.setAttribute("contenteditable", "false");
  score.setAttribute("contenteditable", "false");
  status.innerHTML = `<td class='status' id='status-${row_id}'>${capitalizeFirstLetter(
    status_fr
  )}</td>`;
  edit_btn.innerHTML = `<i onclick='edit_mode(${row_id})' class='fa-solid fa-pencil'></i>`;
  delete_btn.remove();
  update_entry(
    row_id,
    prog.innerHTML.replace(/\D/g, ""),
    score.innerHTML.replace(/\D/g, ""),
    status_fr
  );
};

const update_entry = (id, progress, score, status) => {
  const xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", `${endpoint}edit`);
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlhttp.send(
    JSON.stringify({ media_type: type, media_id: id, progress, score, status })
  );
};

const filter_buttons = () => {
  document.getElementById("current").addEventListener("click", () => {
    hide_except("current");
  });
  document.getElementById("completed").addEventListener("click", () => {
    hide_except("completed");
  });
  document.getElementById("paused").addEventListener("click", () => {
    hide_except("paused");
  });
  document.getElementById("dropped").addEventListener("click", () => {
    hide_except("dropped");
  });
  document.getElementById("planning").addEventListener("click", () => {
    hide_except("planning");
  });
  document.getElementById("all").addEventListener("click", () => {
    hide_except("all");
  });
};

const hide_except = (type) => {
  const table = document.getElementById("mediaTable");
  const rows = table.rows;
  for (let i = 0; i < rows.length; i++) {
    if (rows[i].id !== "headers") {
      if (type === "all") {
        rows[i].style.display = "";
      } else {
        if (rows[i].className !== type) {
          rows[i].style.display = "none";
        } else {
          rows[i].style.display = "";
        }
      }
    }
  }
};

const show_count = (type) => {
  const table = document.getElementById("mediaTable");
  const rows = table.rows;
  const elem = document.getElementById(type);

  if (type === "all") {
    elem.innerHTML = `${capitalizeFirstLetter(type)} (${rows.length - 1})`;
  } else {
    let count = 0;
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].id !== "headers") {
        if (rows[i].className === type) {
          count++;
        }
      }
    }
    elem.innerHTML = `${capitalizeFirstLetter(type)} (${count})`;
  }
};

function render_table(resp, table) {
  // Clear the existing rows
  while (table.rows.length > 0) {
    table.deleteRow(0);
  }

  // Add headers row
  headers = table.insertRow();
  headers.id = "headers";
  headers.insertCell(0);
  headers.insertCell(1).outerHTML = "<th align='left'>Title</th>";
  headers.insertCell(2).outerHTML = "<th align='left'>Status</th>";
  headers.insertCell(3).outerHTML = "<th>Progress</th>";
  headers.insertCell(4).outerHTML = "<th>Score</th>";

  // Add the rows for each media item
  for (let i = 0; i < resp.length; i++) {
    var row = table.insertRow();
    row.id = resp[i].media_id;
    row.className = resp[i].status.toLowerCase();

    var link = "https://anilist.co/" + type + "/" + resp[i].media_id;

    // Create a new <a> element to use as the link instead of using setAttribute
    var _img = (row.insertCell(
      0
    ).innerHTML = `<img class='cover-icon' id='${row.id}' src='${resp[i].image}'>`);
    var title = row.insertCell(1);
    var titleLink = document.createElement("a");
    titleLink.href = link;
    titleLink.className = "title";
    titleLink.id = "title-" + row.id;
    titleLink.innerText = resp[i].title;
    title.appendChild(titleLink);

    var status = (row.insertCell(2).outerHTML = `<td id='status-${
      row.id
    }'>${capitalizeFirstLetter(resp[i].status)}</td>`);
    var prog = (row.insertCell(
      3
    ).outerHTML = `<td class='center' id='progress-${row.id}'>${resp[i].progress}</td>`);

    var score = row.insertCell(4);
    var scoreInnerHTML = "";
    if (rating_type === "stars") {
      scoreInnerHTML = `${resp[i].score} <i class='fa-solid fa-star'></i>`;
    } else {
      scoreInnerHTML = `${resp[i].score}`;
    }
    score.innerHTML = `<td class='center' id='score-${row.id}'>${scoreInnerHTML}</td>`;

    var edit_btn = row.insertCell(5);
    edit_btn.innerHTML = `<i onclick='edit_mode(${row.id})' class='fa-solid fa-pencil'></i>`;
  }
}

const get_list = () => {
  $.getJSON(`${endpoint}list/${type}`, (resp, status) => {
    const table = document.getElementById("mediaTable");
    const headers = table.insertRow(0);
    headers.id = "headers";
    headers.insertCell(0);
    headers.insertCell(1).outerHTML = "<th align='left'>Title</th>";
    headers.insertCell(2).outerHTML = "<th align='left'>Status</th>";
    headers.insertCell(3).outerHTML = "<th>Progress</th>";
    headers.insertCell(4).outerHTML = "<th>Score</th>";
    render_table(resp, table);
    filter_buttons();
    hide_except("current");
    const types = [
      "current",
      "completed",
      "paused",
      "dropped",
      "planning",
      "all",
    ];
    types.forEach((type) => {
      show_count(type);
    });
  });
};

window.addEventListener("load", () => {
  get_rating_type();
});

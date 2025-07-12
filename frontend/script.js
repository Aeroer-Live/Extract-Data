let companyData = [];

function uploadFile() {
  const input = document.getElementById("fileInput");
  const file = input.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  fetch("http://localhost:5000/upload", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      companyData = data;
      showData(data);
      document.getElementById("buttons").style.display = "block";
    });
}

function showData(data) {
  const table = document.getElementById("dataTable");
  table.innerHTML = "";

  if (!data.length) return;

  const headers = Object.keys(data[0]);
  const thead = table.insertRow();
  headers.forEach(h => {
    const th = document.createElement("th");
    th.innerText = h;
    thead.appendChild(th);
  });

  data.forEach(row => {
    const tr = table.insertRow();
    headers.forEach(h => {
      const td = tr.insertCell();
      td.innerText = row[h] || "";
    });
  });
}

function downloadPDF() {
  html2pdf().from(document.getElementById("dataTable")).save("data.pdf");
}

function downloadExcel() {
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(companyData);
  XLSX.utils.book_append_sheet(wb, ws, "CompanyData");
  XLSX.writeFile(wb, "data.xlsx");
}
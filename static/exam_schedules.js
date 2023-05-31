document.addEventListener("DOMContentLoaded", function () {
  var currentPage = 1;
  var rowsPerPage = 100;
  var rows = Array.from(
    document.getElementsByTagName("tbody")[0].getElementsByTagName("tr")
  );
  var totalPages = Math.ceil(rows.length / rowsPerPage);

  function showPage(pageNumber) {
    var startIndex = (pageNumber - 1) * rowsPerPage;
    var endIndex = startIndex + rowsPerPage;

    rows.forEach(function (row, index) {
      if (index >= startIndex && index < endIndex) {
        row.style.display = "table-row";
      } else {
        row.style.display = "none";
      }
    });

    document.getElementById("currentPage").textContent = pageNumber;
  }

  function goToPrevPage() {
    if (currentPage > 1) {
      currentPage--;
      showPage(currentPage);
    }
  }

  function goToNextPage() {
    if (currentPage < totalPages) {
      currentPage++;
      showPage(currentPage);
    }
  }

  document.getElementById("prevPage").addEventListener("click", goToPrevPage);
  document.getElementById("nextPage").addEventListener("click", goToNextPage);

  showPage(currentPage);
});

function getRowValue(row, role) {
  var index = row.getAttribute("data-row-index");
  var url = "/openStudentReservationScreen";
  if (role == "teacher") {
    url = "/openTeacherReservationScreen";
  } else if (role == "it_staff") {
    url = "/openITStaffReservationScreen";
  } else if (role == "student") {
    url = "/openStudentReservationScreen";
  } else {
    url = "/openStudentReservationScreen";
  }
  window.location.href = url + "?row_index_of_selected_class=" + index;
}

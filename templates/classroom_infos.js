function getRowValue(row) {
  var index = row.getAttribute("data-row-index");
  var url = "/openStudentReservationScreen";
  var role = "{{session['role']}}";
  if (role == "student") {
    url = "/openStudentReservationScreen";
  } else if (role == "teacher") {
    url = "/openTeacherReservationScreen";
  } else if (role == "it_staff") {
    url = "/openITStaffReservationScreen";
  }

  window.location.href = url + "?row_index_of_selected_class=" + index;
}

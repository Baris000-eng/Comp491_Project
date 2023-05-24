const allReservationsRadio = document.getElementById('allReservations');
const myReservationsRadio = document.getElementById('myReservations');
const recordChangesButton = document.querySelector('.filterReservations button');

recordChangesButton.addEventListener('click', function(event) {
  event.preventDefault();
  if (allReservationsRadio.checked) {
    allReservationsRadio.checked = true;
    myReservationsRadio.checked = false;
  } else if (myReservationsRadio.checked) {
    allReservationsRadio.checked = false;
    myReservationsRadio.checked = true;
  }
});


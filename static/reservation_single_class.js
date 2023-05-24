const allReservationsRadio = document.getElementById('allReservations');
const myReservationsRadio = document.getElementById('myReservations');

myReservationsRadio.addEventListener('click', function() {
        allReservationsRadio.checked = false;
        myReservationsRadio.checked = true;
});
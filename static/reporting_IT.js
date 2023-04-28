window.onload=function(){
    var iso_str = new Date().toISOString();
    var splitted = iso_str.split('T');
    var today = splitted[0];
    var date_element = document.getElementsByName("date");
    var obtained_date = date_element[0];
    obtained_date.setAttribute('min', today);
  }
  
  
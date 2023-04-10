// get the combobox element and its options
const comboBox = document.querySelector('.combo-box');
const options = comboBox.querySelectorAll('option');

// add an event listener to the combobox
comboBox.addEventListener('input', () => {
  const searchText = comboBox.value.toLowerCase();

  // filter the options based on the search text
  const filteredOptions = Array.from(options)
    .filter(option => option.textContent.toLowerCase().startsWith(searchText));

  // update the combobox dropdown with the filtered options
  const dropdown = comboBox.querySelector('select');
  dropdown.innerHTML = '';
  filteredOptions.forEach(option => dropdown.appendChild(option));
});

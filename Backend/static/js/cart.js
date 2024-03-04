let updateBtns = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", () => {
    let productId = updateBtns[i].dataset.product;
    let action = updateBtns[i].dataset.action;
    updateUserOrder(productId, action);
  });
}

function updateUserOrder(productId, action) {
  let url = "/update-item/";
  // whenever we are sending POST data we need to set csrf_token in django
  fetch(url, {
    //url define which url to send data
    method: "POST", // define what kind of data to send: type = POST data, headers -> object, body -> data send to backend
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }), //-> send data as string
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(`data:`, data);
      location.reload()
    });
}


document.addEventListener('DOMContentLoaded', function() {
  var today = new Date();
  var tomorrow = new Date();
  tomorrow.setDate(today.getDate() + 1);

  // Format dates as YYYY-MM-DD
  var todayFormatted = today.toISOString().split('T')[0];
  var tomorrowFormatted = tomorrow.toISOString().split('T')[0];

  // Set today's and tomorrow's dates as options in the delivery date dropdown
  document.getElementById('deliveryDate').innerHTML = `
      <option value="${todayFormatted}">${todayFormatted}</option>
      <option value="${tomorrowFormatted}">${tomorrowFormatted}</option>
  `;
});

document.addEventListener('DOMContentLoaded', function() {
  var timeSelect = document.getElementById('deliveryTime');

  // Define start and end time
  var startTime = 9; // 9 am
  var endTime = 21; // 9 pm

  // Generate time options
  for (var hour = startTime; hour < endTime; hour++) {
      var startHour = hour < 10 ? '0' + hour : hour; // Add leading zero if hour is single digit
      var endHour = (hour + 1) < 10 ? '0' + (hour + 1) : (hour + 1); // Add leading zero if hour is single digit

      var optionText = startHour + ':00 - ' + endHour + ':00';
      var optionValue = startHour + ':00-' + endHour + ':00';

      // Create an option element
      var option = document.createElement('option');
      option.value = optionValue;
      option.textContent = optionText;

      // Append the option to the select element
      timeSelect.appendChild(option);
  }
});
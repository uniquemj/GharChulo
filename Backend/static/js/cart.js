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

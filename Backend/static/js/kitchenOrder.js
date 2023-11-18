let saveBtn = document.getElementsByClassName("save-btn");
let orderStatus = document.getElementsByName("order_status");
let completed = document.getElementsByName("is_completed");

for (let i = 0; i < saveBtn.length; i++) {
  saveBtn[i].addEventListener("click", () => {
    let complete;
    let orderId = saveBtn[i].dataset.order;
    let action = saveBtn[i].dataset.action;

    let order_status = orderStatus[i].value;
    console.log(orderStatus[i]);
    if (completed[i].checked) {
      complete = true;
    } else {
      complete = false;
    }
    let is_completed = complete;
    console.log(complete);
    updateOrder(orderId, action, order_status, is_completed);
  });
}

const updateOrder = (orderId, action, order_status, is_completed) => {
  url = "/update-order/";

  $.ajax({
    type: "POST",
    url: url,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: {
      orderId: orderId,
      action: action,
      order_status: order_status,
      is_completed: is_completed,
    },
    dataType: "json",
    success: function (data) {
      console.log("data: ", data);
      location.reload()
    },
    failure: function () {
      console.log("Order Update Failed");
    },
  });
};

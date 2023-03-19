$(document).ready(function () {
  $(".view-commodity-button").click(function () {
    console.log($(this).attr("value"));
  });

  $(".add-to-cart-button").click(function (event) {
    event.preventDefault();
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const idAttr = $(this).attr("id");
    const idNumber = idAttr.match(/\d+/)[0];
    let inputQuantity = $("#inputQuantity").val();
    inputQuantity = isNaN(inputQuantity) ? 1 : inputQuantity;
    $.post(
      "/add_to_cart/",
      { csrfmiddlewaretoken: csrfToken, c_id: idNumber, amount: inputQuantity },
      function (data) {
        if (!data.authenticated) {
          window.location.href = "/login/";
        } else {
          $(".shopping-cart-count").html(data.total_items);
          $("#sucess-modal").modal("show");
        }
      }
    );
  });

  $("#remove-all-from-cart-button, .remove-from-cart").click(function (event) {
    event.preventDefault();
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const itemID = $(this).attr("data-id");

    $.ajax({
      url: "/remove_from_cart/",
      type: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        itemID,
      },
      success: function (data) {
        window.location.href = "/cart/";
      },
    });
  });
});

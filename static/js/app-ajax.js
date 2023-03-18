$(document).ready(function () {
  $(".view-commodity-button").click(function () {
    console.log($(this).attr("value"));
  });

  $(".add-to-cart-button").click(function (event) {
    event.preventDefault()
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const idAttr = $(this).attr("id");
    const idNumber = (idAttr.match(/\d+/)[0]);
    let inputQuantity = ($('#inputQuantity').val());
    inputQuantity = isNaN(inputQuantity) ? 1 : (inputQuantity);
    $.post(
      "/add_to_cart/",
      { csrfmiddlewaretoken: csrfToken, c_id: idNumber, amount: inputQuantity },
      function (data) {
        $(".shopping-cart-count").html(data);
        $("#sucess-modal").modal("show");
      }
    );
  });
});

$(document).ready(function () {
  $(".view-commodity-button").click(function () {
    console.log($(this).attr("value"));
  });

  $(".add-to-cart-button").click(function () {
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const idAttr = ($(this).attr('id'))
    const idNumber = parseInt(idAttr.match(/\d+/)[0]);
    $.post(
      "/add_to_cart/",
      { 'csrfmiddlewaretoken': csrfToken, 'c_id': idNumber },
      function (data) {
        $('.shopping-cart-count').html(data);
        $('#sucess-modal').modal('show')
      }
    );
  });
});

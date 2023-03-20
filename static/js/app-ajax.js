$(document).ready(function () {
  $(".add-to-cart-button").click(function (event) {
    event.preventDefault();
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const idAttr = $(this).attr("id");
    const idNumber = idAttr.match(/\d+/)[0];
    let inputQuantity = $("#inputQuantity").val();
    inputQuantity = isNaN(inputQuantity)
      ? 1
      : inputQuantity < 1
      ? 1
      : inputQuantity;
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

  $("#update-cart").click(function (event) {
    event.preventDefault();
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    let cart_items = [];

    $(".cart-item").each(function () {
      const itemId = $(this).find(".remove-from-cart").data("id");
      let quantity = $(this).find("#inputQuantity").val();
      quantity = isNaN(quantity) ? 1 : quantity < 1 ? 1 : quantity;
      cart_items.push({
        itemId,
        quantity,
      });
    });
    console.log(cart_items);

    $.ajax({
      url: "/update_cart/",
      type: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        cart_items: JSON.stringify(cart_items),
      },
      success: function (data) {
        window.location.href = "/cart/";
      },
    });
  });

  $("#checkout-cart").click(function (event) {
    event.preventDefault();
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    console.log("check out");
    $.ajax({
      url: "/checkout_cart/",
      type: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
      },
      success: function (data) {
        $("#sucess-modal").find(".modal-body").text(data);
        $("#sucess-modal").modal("show");
        setTimeout(() => {
          window.location.href = "/cart/";
        }, 2000);
      },
      error: function (xhr, status, error) {
        const errorMessage = xhr.responseJSON.error;
        $("#error-modal").find(".modal-body").text(errorMessage);
        $("#error-modal").modal("show");
      },
    });
  });

  $("#file-upload").change(function (event) {
    // Get the selected file
    const selectedFile = event.target.files[0];
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const formData = new FormData();
    formData.append('picture', selectedFile);
    $.ajax({
      url: "/upload_profile_image/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      headers: {
        "X-CSRFToken": csrfToken
      },
      success: function (data) {
        // Handle success response
        $(".img-account-profile").attr("src", data.image_url);
      },
      error: function (xhr, status, error) {
        // Handle error response
      }
    });
  });
});

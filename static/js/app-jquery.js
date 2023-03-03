$(document).ready(function() {
    var pathname = $(location).attr('pathname')
    if (pathname === "/") {
        $('#nav-link-home').addClass('active')
    } else if (pathname === "/search/") {
        $('#nav-link-search').addClass('active')
    } else {
        $('.nav-link').removeClass('active')
    }

    $('.search-button').click(function() {
        alert('Jquery')
    })
    
});
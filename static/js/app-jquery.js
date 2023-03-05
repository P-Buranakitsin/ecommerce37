$(document).ready(function() {
    let pathname = $(location).attr('pathname')
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

    /* Force profile tab in profile.html to become active */
    $('#nav-profile-tab').addClass('show active')
    $('#nav-profile').addClass('show active')
});
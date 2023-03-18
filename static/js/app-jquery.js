$(document).ready(function() {
    let pathname = $(location).attr('pathname')
    if (pathname === "/") {
        $('#nav-link-home').addClass('active')
    } else if (pathname.includes("/search/")) {
        $('#nav-link-search').addClass('active')
    } else if (pathname.includes("/contactUs/")) {
        $('#nav-link-contact-us').addClass('active')
        $('main').addClass('d-flex flex-column flex-grow-1 justify-content-center')
    } else {
        $('.nav-link').removeClass('active')
    }
    /* Add class show active whenever class sohw_tab presents */
    $('.show_tab').addClass('show active')
});
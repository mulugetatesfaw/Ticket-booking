if (window.location.pathname === "/home" || window.location.pathname === "/") {
    $('li#filter-nav').show();
} else {
    $('li#filter-nav').hide();
}

if (window.location.pathname === "/about" || window.location.pathname === "/home" || window.location.pathname === "/"){
    $('li#contact-nav').show();
} else {
    $('li#contact-nav').hide();
}
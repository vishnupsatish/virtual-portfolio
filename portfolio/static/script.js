

$(document).ready(function () {
    $('.carousel').carousel();
    $('.fixed-action-btn').floatingActionButton();
    $('.datepicker').datepicker();
    $('.chips').chips();
    $('.parallax').parallax();
});

function show(id) {
    elem = document.getElementById(id)
    console.log(elem.style.display)
    if (elem.style.display == "none") {
        elem.style.display = "block"
    }
    else {
        elem.style.display = "none"
    }
}
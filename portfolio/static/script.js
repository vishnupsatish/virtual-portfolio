

$(document).ready(function () {
    $('.carousel').carousel();
    $('.fixed-action-btn').floatingActionButton();
    $('.datepicker').datepicker();
    $('.chips').chips();
    $('.parallax').parallax();
    $("#job-form").css('display', "none");
    $("#achievement-form").css('display', "none");
    $("#project-form").css('display', "none");
});

function show(id) {
    elem = document.getElementById(id)
    console.log($("#" + id).css('display'))
    if (($("#" + id).css('display')) === "none") {
        $("#" + id).css('display', "block");
    }
    else {
        $("#" + id).css('display', "none");
    }
}
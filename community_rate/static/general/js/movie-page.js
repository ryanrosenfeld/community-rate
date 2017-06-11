var prevEm = null;



function showForm() {
    $("#update-form").css("display", "inline-block");
}

function hideForm() {
    $("#update-form").css("display", "none");
}

function setReaction(em) {
    var s = "em " + "em-" + em;
    $("#reaction-field").val(s);
    $(prevEm).css("border", "none");
    var sel = ".em-" + em;
    $(sel).css("border", "solid #18BC9C 3px");
    $(sel).css("border-radius", "5px");
    prevEm = sel;
}
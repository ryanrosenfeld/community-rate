function toggleEditProfileDisplay() {
    if ($("#edit-profile").css("display") == "none") {
        $("#edit-profile").css("display", "inline-block");
        $("#update-pic").css("display", "none");
    }
    else {
        $("#edit-profile").css("display", "none");
    }
}

function toggleUpdatePicDisplay() {
    if ($("#update-pic").css("display") == "none") {
        $("#update-pic").css("display", "inline-block");
        $("#edit-profile").css("display", "none")
    }
    else {
        $("#update-pic").css("display", "none");
    }
}
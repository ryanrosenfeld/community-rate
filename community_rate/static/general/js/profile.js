function toggleEditProfileDisplay() {
    if ($("#edit-profile").css("display") == "none") {
        $("#edit-profile").css("display", "inline-block");
    }
    else {
        $("#edit-profile").css("display", "none");
    }
}
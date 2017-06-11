var newPic = '';

// Prepare the preview for profile picture
$("#wizard-picture").change(function () {
    var files = document.getElementById("wizard-picture").files;
    var file = files[0];
    if (!file) {
        functions.sweetAlert("warning", "No image selected");
        return null;
    }
    if (!(file.type == "image/jpeg" || file.type == "image/png")) {
        functions.sweetAlert("warning", "Please choose a .jpeg or .png file");
        return null;
    }
    readURL(this);
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#profPicPreview').attr('src', e.target.result).fadeIn('slow');
            newPic = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function tempUpdateProfPic() {
    $('#sidebarProfPic').attr('src', newPic).fadeIn('slow');
    $('#profPic').attr('src', newPic).fadeIn('slow');
}

function showEditProfile() {
    $("#editProfileModal").modal();
}

function showUpdatePic() {
    $("#updatePicModal").modal();
}

function updatePic() {
    var files = document.getElementById("wizard-picture").files;
    var file = files[0];
    if (!file) {
        functions.sweetAlert("warning", "No image selected");
        return null;
    }
    if (!(file.type == "image/jpeg" || file.type == "image/png")) {
        functions.sweetAlert("warning", "Please choose a .jpeg or .png file");
        return null;
    }
    functions.uploadFile(file);
    $("#updatePicModal").modal('toggle');
    tempUpdateProfPic();
}
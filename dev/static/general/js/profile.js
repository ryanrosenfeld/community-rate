$(document).ready(function() {
    checkToShowModals()
});

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

function checkToShowModals() {
    var url = window.location.href;
    if (url.indexOf("?modal=edit") != -1) {
        showEditProfile();
    }
    if (url.indexOf("?modal=picture") != -1) {
        showUpdatePic();
    }

}

$("#updatePicModal").on("shown.bs.modal", function () {
    $("#edit-profile-pic").croppie('bind', {
        url: currentPic
    });
});

$("#profile-pic-upload").change(function () {
    var fr = new FileReader();

    fr.onload = function (e) {
        newPic = e.target.result;

        $("#edit-profile-pic").croppie('bind', {
            url: e.target.result
        });
    };
    fr.readAsDataURL(this.files[0]);
});

function updatePic() {
    profileInput.croppie('result', {
        type: 'canvas',
        size: 'viewport'
    }).then(function (img) {
        functions.saveProfilePic(img);
        $("#updatePicModal").modal('toggle');
        newPic = img;
        currentPic = img;
        tempUpdateProfPic();
    })
}
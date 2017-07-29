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

function initCroppie() {
    var $img = $("#croppieImg");

    $img.croppie({
        viewport: {
            width: 150,
            height: 150,
            type: 'circle'
        },
        boundary: {
            width: 200,
            height: 200
        }
    });
    $img.croppie('bind', imgUrl);

    $("#btn-update-pic").on('click', function() {
        $img.croppie('bind');
    })
}

// function updatePic() {
//     var files = document.getElementById("wizard-picture").files;
//     var file = files[0];
//     if (!file) {
//         functions.sweetAlert("warning", "No image selected");
//         return null;
//     }
//     if (!(file.type == "image/jpeg" || file.type == "image/png")) {
//         functions.sweetAlert("warning", "Please choose a .jpeg or .png file");
//         return null;
//     }
//     functions.uploadFile(file);
//     $("#updatePicModal").modal('toggle');
//     tempUpdateProfPic();
// }
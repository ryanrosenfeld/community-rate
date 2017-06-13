$(window).on('load', function () {
    var newUser = "{{ new_user }}";
    if (newUser == "True") {
        $('#welcomeModal').modal({backdrop: 'static', keyboard: false});
    }
    else {
        tutorial(1);
    }
});

function tutorial(step) {
    switch (step) {
        case 1:
            $('#tutorialModal1').modal({backdrop: 'static', keyboard: false});
            $('.sidebar').removeClass('hidden');
            break;
        case 2:
            $('#tutorialModal2').modal({backdrop: 'static', keyboard: false});
            $('.sidebar').removeClass('hidden');
            $('.navbar').removeClass('hidden');
            break;
        case 3:
            $('.wizard-container').removeClass('hidden');
            $('.sidebar').removeClass('hidden');
            $('.navbar').removeClass('hidden');
            functions.initMaterialWizard();
            break;
    }

}
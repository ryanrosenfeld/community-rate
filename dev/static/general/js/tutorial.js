function tutorial(step) {
    // If on mobile device skip straight to profile setup
    if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        step = 3;
    }
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
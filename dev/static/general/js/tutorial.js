function tutorial(step) {
    // If on mobile device skip straight to profile setup
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
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
            initMaterialWizard();

            $("#edit-profile-pic").croppie('bind', {
                url: defaultPic
            });
            break;
    }

}

$("#profile-pic-upload").change(function () {
    var fr = new FileReader();

    fr.onload = function (e) {
        profileInput.croppie('bind', {
            url: e.target.result
        });
    };
    fr.readAsDataURL(this.files[0]);
});

function updatePic() {
    profileInput.croppie('result', {
        type: 'canvas',
        size: 'viewport'
    }).then(function (thepicture) {
        functions.saveProfilePic(thepicture);
        $("#sidebarProfPic").attr('src', thepicture);
    })
}

function initMaterialWizard() {
    // Code for the Validator
    var $validator = $('.wizard-card form').validate({
        rules: {
            timezone: {
                required: true
            }
        },

        errorPlacement: function (error, element) {
            $(element).parent('div').addClass('has-error');
        }
    });

    // Wizard Initialization
    $('.wizard-card').bootstrapWizard({
        'tabClass': 'nav nav-pills',
        'nextSelector': '.btn-next',
        'previousSelector': '.btn-previous',

        onNext: function (tab, navigation, index) {
            updatePic();
        },

        onInit: function (tab, navigation, index) {
            //check number of tabs and fill the entire row
            var $total = navigation.find('li').length;
            $width = 100 / $total;
            var $wizard = navigation.closest('.wizard-card');

            $display_width = $(document).width();

            if ($display_width < 600 && $total > 3) {
                $width = 50;
            }

            navigation.find('li').css('width', $width + '%');
            $first_li = navigation.find('li:first-child a').html();
            $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
            $('.wizard-card .wizard-navigation').append($moving_div);
            refreshAnimation($wizard, index);
            $('.moving-tab').css('transition', 'transform 0s');
        },

        onTabClick: function (tab, navigation, index) {
            var $valid = $('.wizard-card form').valid();
        },

        onTabShow: function (tab, navigation, index) {
            var $total = navigation.find('li').length;
            var $current = index + 1;

            var $wizard = navigation.closest('.wizard-card');

            // If it's the last tab then hide the last button and show the finish instead
            if ($current >= $total) {
                $($wizard).find('.btn-next').hide();
                $($wizard).find('.btn-finish').show();
            } else {
                $($wizard).find('.btn-next').show();
                $($wizard).find('.btn-finish').hide();
            }

            button_text = navigation.find('li:nth-child(' + $current + ') a').html();

            setTimeout(function () {
                $('.moving-tab').text(button_text);
            }, 150);

            var checkbox = $('.footer-checkbox');

            if (!index == 0) {
                $(checkbox).css({
                    'opacity': '0',
                    'visibility': 'hidden',
                    'position': 'absolute'
                });
            } else {
                $(checkbox).css({
                    'opacity': '1',
                    'visibility': 'visible'
                });
            }

            refreshAnimation($wizard, index);
        }
    });

    $('.set-full-height').css('height', 'auto');

    $(window).resize(function () {
        $('.wizard-card').each(function () {
            $wizard = $(this);
            index = $wizard.bootstrapWizard('currentIndex');
            refreshAnimation($wizard, index);

            $('.moving-tab').css({
                'transition': 'transform 0s'
            });
        });
    });

    function refreshAnimation($wizard, index) {
        total_steps = $wizard.find('li').length;
        move_distance = $wizard.width() / total_steps;
        step_width = move_distance;
        move_distance *= index;

        $current = index + 1;

        if ($current == 1) {
            move_distance -= 8;
        } else if ($current == total_steps) {
            move_distance += 8;
        }

        $wizard.find('.moving-tab').css('width', step_width);
        $('.moving-tab').css({
            'transform': 'translate3d(' + move_distance + 'px, 0, 0)',
            'transition': 'all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1)'
        });
    }
}
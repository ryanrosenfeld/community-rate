functions = {
    sweetAlert: function (type, message, onConfirmFunction) {

        if (type == 'success') {
            swal({
                title: message,
                buttonsStyling: false,
                confirmButtonClass: "btn btn-success",
                type: "success"
            });
        }
        else if (type == "warning") {
            swal({
                title: message,
                buttonStyling: false,
                confirmButtonClass: 'btn btn-info',
                type: "warning"
            })
        }
        else if (type == 'welcome') {
            swal({
                title: 'You\'re all set!',
                html: 'Please reach out to <i class="text-warning">ryro003@gmail.com</i> if you have any further ' +
                'questions. You\'re currently at the <strong>Activity Feed</strong>, which will be blank until you follow some friends. ' +
                'Send out those follows, start rating movies in the <strong>Movie Database</strong>, and enjoy the site!',
                buttonsStyling: false,
                confirmButtonClass: 'btn btn-success',
                type: "success"
            })
        }
        else if (type == 'warning-message-and-confirmation') {
            swal({
                    title: 'Are you sure?',
                    text: message,
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonClass: 'btn btn-success',
                    cancelButtonClass: 'btn btn-danger',
                    confirmButtonText: 'Yes, delete it!',
                    buttonsStyling: false
                }).then(function() {
                        onConfirmFunction();
                    });
    	}
    },

    follow: function (username, name, onSuccess, user_id) {
        $.ajax({
            url: '/ajax/follow/',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    functions.sweetAlert('success', "Successfully followed " + name);
                    if (user_id != null) {
                        onSuccess(username, name, user_id);
                    }
                    else {
                        onSuccess(username, name);
                    }
                }
                else {
                    functions.sweetAlert('problem');
                }
            }
        });
    },

    unfollow: function (username, name, onSuccess, user_id) {
        $.ajax({
            url: '/ajax/unfollow/',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    functions.sweetAlert('success', "Successfully unfollowed " + name);
                    if (user_id != null) {
                        onSuccess(username, name, user_id);
                    }
                    else {
                        onSuccess(username, name);
                    }

                }
                else {
                    functions.sweetAlert('warning', "There was a problem.");
                }
            }
        });
    },

    markNotificationsRead: function() {
        $.ajax({
            url: '/ajax/mark-notifications-read/'
        });
        $("#numRead").html('0');
    },

    checkHamburgerMenu: function() {
        if ($(window).width() <= 991) {
            return true;
        }
        return false;
    },

    uploadFile: function(file) {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
      xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
          if(xhr.status === 200){
            var response = JSON.parse(xhr.responseText);
            upload(file, response.data, response.url);
          }
          else{
            functions.sweetAlert("warning", "There was a problem with upload");
          }
        }
      };
      xhr.send();

      function upload(file, s3Data, url) {
          var xhr = new XMLHttpRequest();
          xhr.open("POST", s3Data.url);

          var postData = new FormData();
          for(key in s3Data.fields){
            postData.append(key, s3Data.fields[key]);
          }
          postData.append('file', file);

          xhr.onreadystatechange = function() {
            if(xhr.readyState === 4){
              if(xhr.status === 200 || xhr.status === 204){
                // success
                  alert("Success");
              }
              else{
                // failure (but this seems to always be the case and it still works ??)
              }
           }
          };
          xhr.send(postData);

          // Send ajax request to reflect the user now has a picture
          $.ajax({
            url: '/ajax/has-pic/'
          });
      }
    },

    initMaterialWizard: function(){
        // Code for the Validator
        var $validator = $('.wizard-card form').validate({
    		  rules: {
    		    timezone: {
    		      required: true
    		    }
            },

            errorPlacement: function(error, element) {
                $(element).parent('div').addClass('has-error');
             }
    	});

        // Wizard Initialization
      	$('.wizard-card').bootstrapWizard({
            'tabClass': 'nav nav-pills',
            'nextSelector': '.btn-next',
            'previousSelector': '.btn-previous',

            onNext: function(tab, navigation, index) {
            	var $valid = $('.wizard-card form').valid();
            	if(!$valid) {
            		$validator.focusInvalid();
            		return false;
            	}
            },

            onInit : function(tab, navigation, index){

              //check number of tabs and fill the entire row
              var $total = navigation.find('li').length;
              $width = 100/$total;
              var $wizard = navigation.closest('.wizard-card');

              $display_width = $(document).width();

              if($display_width < 600 && $total > 3){
                  $width = 50;
              }

               navigation.find('li').css('width',$width + '%');
               $first_li = navigation.find('li:first-child a').html();
               $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
               $('.wizard-card .wizard-navigation').append($moving_div);
               refreshAnimation($wizard, index);
               $('.moving-tab').css('transition','transform 0s');
           },

            onTabClick : function(tab, navigation, index){
                var $valid = $('.wizard-card form').valid();

                // if(!$valid){
                //     return false;
                // } else{
                //     return true;
                // }
                // return true;
            },

            onTabShow: function(tab, navigation, index) {
                var $total = navigation.find('li').length;
                var $current = index+1;

                var $wizard = navigation.closest('.wizard-card');

                // If it's the last tab then hide the last button and show the finish instead
                if($current >= $total) {
                    $($wizard).find('.btn-next').hide();
                    $($wizard).find('.btn-finish').show();
                } else {
                    $($wizard).find('.btn-next').show();
                    $($wizard).find('.btn-finish').hide();
                }

                button_text = navigation.find('li:nth-child(' + $current + ') a').html();

                setTimeout(function(){
                    $('.moving-tab').text(button_text);
                }, 150);

                var checkbox = $('.footer-checkbox');

                if( !index == 0 ){
                    $(checkbox).css({
                        'opacity':'0',
                        'visibility':'hidden',
                        'position':'absolute'
                    });
                } else {
                    $(checkbox).css({
                        'opacity':'1',
                        'visibility':'visible'
                    });
                }

                refreshAnimation($wizard, index);
            }
      	});


        // Prepare the preview for profile picture
        $("#wizard-picture").change(function(){
            var files = document.getElementById("wizard-picture").files;
            var file = files[0];
            if(!file){
                functions.sweetAlert("warning", "No image selected");
                return null;
            }
            if (!(file.type == "image/jpeg" || file.type == "image/png")) {
                functions.sweetAlert("warning", "Please choose a jpeg or png file");
                return null;
            }
            functions.uploadFile(file);
            readURL(this);
        });

        $('[data-toggle="wizard-radio"]').click(function(){
            wizard = $(this).closest('.wizard-card');
            wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
            $(this).addClass('active');
            $(wizard).find('[type="radio"]').removeAttr('checked');
            $(this).find('[type="radio"]').attr('checked','true');
        });

        $('[data-toggle="wizard-checkbox"]').click(function(){
            if( $(this).hasClass('active')){
                $(this).removeClass('active');
                $(this).find('[type="checkbox"]').removeAttr('checked');
            } else {
                $(this).addClass('active');
                $(this).find('[type="checkbox"]').attr('checked','true');
            }
        });

        $('.set-full-height').css('height', 'auto');

         //Function to show image before upload

        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        $(window).resize(function(){
            $('.wizard-card').each(function(){
                $wizard = $(this);
                index = $wizard.bootstrapWizard('currentIndex');
                refreshAnimation($wizard, index);

                $('.moving-tab').css({
                    'transition': 'transform 0s'
                });
            });
        });

        function refreshAnimation($wizard, index){
            total_steps = $wizard.find('li').length;
            move_distance = $wizard.width() / total_steps;
            step_width = move_distance;
            move_distance *= index;

            $current = index + 1;

            if($current == 1){
                move_distance -= 8;
            } else if($current == total_steps){
                move_distance += 8;
            }

            $wizard.find('.moving-tab').css('width', step_width);
            $('.moving-tab').css({
                'transform':'translate3d(' + move_distance + 'px, 0, 0)',
                'transition': 'all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1)'

            });
        }
    }

};
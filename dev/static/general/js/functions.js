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
        else if (type == 'info') {
            if (onConfirmFunction != null) {
                swal({
                    html: message,
                    buttonStyling: false,
                    confirmButtonClass: 'btn btn-info',
                    type: "info"
                }).then(function() {
                    onConfirmFunction();
                })
            }
            else {
                swal({
                    html: message,
                    buttonStyling: false,
                    confirmButtonClass: 'btn btn-info',
                    type: "info"
                })
            }

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
            }).then(function () {
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

    markNotificationsRead: function () {
        $.ajax({
            url: '/ajax/mark-notifications-read/'
        });
        $("#numRead").html('0');
    },

    checkHamburgerMenu: function () {
        if ($(window).width() <= 991) {
            return true;
        }
        return false;
    },

    // Requires inclusion of jquery.cookie.js script
    saveProfilePic: function (base64String) {
        functions.preparePostToken();

        $.ajax({
            url: "/ajax/upload-profile-pic/",
            data: {
                pic: base64String
            },
            dataType: 'json',
            type: "POST"
        })
    },

    // Requires inclusion of jquery.cookie.js script
    preparePostToken: function () {
        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    },

    checkBrowser: function () {
        // Opera 8.0+
        if ((!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0) {
            return "opera"
        }
        // Firefox 1.0+
        if (typeof InstallTrigger !== 'undefined') {
            return "firefox"
        }
        // Safari 3.0+ "[object HTMLElementConstructor]"
        if (/constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification))) {
            return "safari"
        }
        // Internet Explorer 6-11
        if (/*@cc_on!@*/false || !!document.documentMode) {
            return "ie"
        }
        // Edge 20+
        else if (!!window.StyleMedia) {
            return "edge"
        }
        // Chrome 1+
        if (!!window.chrome && !!window.chrome.webstore) {
            return "chrome"
        }
    }
};
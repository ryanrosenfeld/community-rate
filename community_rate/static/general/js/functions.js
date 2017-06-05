functions = {
    sweetAlert: function (type, user) {

        if (type == 'follow-success') {
            swal({
                title: "You are now following " + user,
                buttonsStyling: false,
                confirmButtonClass: "btn btn-success",
                type: "success"
            });
        }
        else if (type == 'unfollow-success') {
            swal({
                title: "Successfully unfollowed " + user,
                buttonsStyling: false,
                confirmButtonClass: "btn btn-success",
                type: "success"
            });
        }
        else if (type == 'problem') {
            swal({
                title: 'There was a problem.',
                type: 'warning',
                confirmButtonClass: 'btn btn-success',
                buttonsStyling: false
            })
        }
        else if (type == 'toggle-list-public') {
            swal({
                title: 'Changed list to public',
                buttonsStyling: false,
                confirmButtonClass: 'btn btn-success',
                type: "success"
            })
        }
        else if (type == 'toggle-list-private') {
            swal({
                title: 'Changed list to private',
                buttonsStyling: false,
                confirmButtonClass: 'btn btn-success',
                type: "success"
            })
        }
        else if (type == 'update-list-name') {
            swal({
                title: 'Changed list name',
                buttonsStyling: false,
                confirmButtonClass: 'btn btn-success',
                type: "success"
            })
        }
    },

    follow: function (username, name, onSuccess) {
        $.ajax({
            url: '/ajax/follow/',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    functions.sweetAlert('follow-success', name);
                    onSuccess(username, name);
                }
                else {
                    functions.sweetAlert('problem');
                }
            }
        });
    },

    unfollow: function (username, name, onSuccess) {
            $.ajax({
                url: '/ajax/unfollow/',
                data: {
                    'username': username
                },
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        functions.sweetAlert('unfollow-success', name);
                        onSuccess(username, name)
                    }
                    else {
                        functions.sweetAlert('problem');
                    }
                }
            });
        }
};
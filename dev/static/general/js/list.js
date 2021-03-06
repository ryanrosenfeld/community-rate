$(document).ready(function() {
    $("#movie-input").keyup(function() {
        if ($(this).val().length > 2) {
            searchMovies();
        }
        else {
            destroyDropdown();
        }
    });

    $("#editor-name").keyup(function() {
        var query = $("#editor-name").val().toLowerCase();
        if (query.length > 0) {
            $('#add-editor-list tr').not('[class*="' + query + '"]').hide();
            $('#add-editor-list tr[class*="' + query + '"]').show();
        }
        else {
            $('#add-editor-list tr').show()
        }
    });
});

function searchMovies() {
    initializeDropdown();
    var query = $("#movie-input").val();
    if (query.length > 2) {
        var index = 0;
        $.ajax({
            url: '/ajax/filter-movies/',
            data: {
                'query': query
            },
            dataType: 'json',
            success: function (data) {
                addMoviesToDropdown(data.results)
            }
        })
    }
}

function initializeDropdown() {
    $("#movie-results").css("display", "inline-block");
    $("#movie-results").html('');
}

function destroyDropdown() {
    $("#movie-results").css("display", "none");
    $("#movie-results").html('');
}

function addMoviesToDropdown(movies) {
    initializeDropdown();
    for (var i = 0; i < movies.length; i++) {
        $("#movie-results").append(
            "<li id='" + movies[i].id + "' onclick='selectMovie(" + movies[i].id + ")'><a>" + movies[i].title + " (" + movies[i].release_date.substring(0,4) + ")</a></li>"
        )
    }
}

function selectMovie(id) {
    addListEntry(id);
    destroyDropdown();
    $("#movie-input").val('');
    $.ajax({
            url: '/ajax/get-movie-info/',
            data: {
                'id': id
            },
            dataType: 'json',
            success: function (data) {
                addMovieRow(data.movie, data.my_rating, data.my_reaction, data.av_rating, data.av_reaction);
            }
        })
}

function addListEntry(movie_id) {
    $.ajax({
        url: '/ajax/add-list-entry/',
            data: {
                'list_id': l_id,
                'movie_id': movie_id
            },
            dataType: 'json'
    })
}

function addMovieRow(movie, my_rating, my_reaction, av_rating, av_reaction) {
    var img_path = "../static/general/img/no_poster.jpg";
    if (movie.poster_path != null) {
        img_path = "http://image.tmdb.org/t/p/w92" + movie.poster_path;
    }
    $("#movie-table-body").append(
        '<tr id="row-' + movie.id + '">' +
            '<td class="td-link" style="pointer-events: none;" onclick=window.location.href="/movie/' + movie.id + '/">' +
                '<div class="img-container">' +
                    '<img src="' + img_path + '" alt="...">' +
                '</div>' +
            '</td>' +
            '<td class="td-name td-link" style="pointer-events: none;" onclick=window.location.href="/movie/' + movie.id + '/">' +
                '<a>' + movie.title + '</a>' +
                '<br />' +
                '<small>' + movie.release_year + '</small>' +
            '</td>' +
            '<td class="text-center td-link" style="pointer-events: none;" onclick=window.location.href="/movie/' + movie.id + '/">' + my_rating + '</td>' +
            '<td class="text-center td-link" style="pointer-events: none;" onclick=window.location.href="/movie/' + movie.id + '/">' + av_rating + '</td>' +
            '<td class="text-center td-link" style="pointer-events: none;" onclick=window.location.href="/movie/' + movie.id + '/"><i class="' + my_reaction + '"></i></td>' +
            '<td class="text-center td-link" style="pointer-events: none;" onclick=window.location.href="/movie/' + movie.id + '/"><i class="' + av_reaction + '"></i></td>' +
            '<td class="text-center edit-display-table" style="display: table-cell">' +
                '<button type="button" id="btn-rmv" class="btn btn-danger btn-simple btn-xs" onclick="removeListItem(' + movie.id + ')">' +
                    '<i class="material-icons">close</i>' +
                '</button>' +
            '</td>' +
        '</tr>'
    );
}

function updateListName() {
    var name = $("#edit-list-name").val();
    if (name != '' && name != $("#list-name").html()) {
        $("#list-name").html(name);
        $.ajax({
            url: '/ajax/update-list-name/',
            data: {
                'list_id': l_id,
                'name': name
            },
            dataType: 'json'
        });
    }
}

function removeListItem(movie_id) {
    $("#row-" + movie_id).remove();
    $.ajax({
        url: '/ajax/remove-list-item/',
        data: {
            'list_id': l_id,
            'movie_id': movie_id
        },
        dataType: 'json'
    })
}

function toggleEditMode() {
    if ($(".edit-display").css("display") == "none") {
        $(".edit-display").css("display", "inline");
        $(".edit-display-table").css("display", "table-cell");
        $(".non-edit-display").css("display", "none");
        $(".td-link").css('pointerEvents', 'none');
        $("table").removeClass('table-hover');
        $("#edit-list-name-group").css("display", "inline-block");
        $("#list-name").css("display", "none");
    }
    else {
        $(".edit-display").css("display", "none");
        $(".edit-display-table").css("display", "none");
        $(".non-edit-display").css("display", "inline");
        $(".td-link").css('pointerEvents', 'auto');
        $("table").addClass('table-hover');
        $("#edit-list-name-group").css("display", "none");
        $("#btn-show-edit-list-name").css("display", "inline-block");
        $("#edit-list-name-group").css("display", "none");
        $("#list-name").css("display", "inline-block");

        // Update list name if it changed
        updateListName();
    }
}

function togglePublicPrivate() {
    var icon = $("#btn-public_private i");
    // var text = $("#btn-public_private").contents(":not(i)");
    var text = $("#btn-public_private span");
    console.log(icon.html());
    if (icon.html() == 'public') {
        icon.html('lock_outline');
        text.html(" Private");
        //functions.sweetAlert('toggle-list-private');
    }
    else {
        icon.html('public');
        text.html(" Public");
        //functions.sweetAlert('toggle-list-public');
    }
    $.ajax({
        url: '/ajax/toggle-public-private/',
        data: {
            'list_id': l_id
        },
        dataType: 'json'
    })
}

function like() {
    $.ajax({
        url: '/ajax/like-list/',
        data: {
            'list_id': l_id
        },
        dataType: 'json',
        success: function(data) {
            if (data.liked) {
                $("#btn-like").html(
                        '<i class="material-icons">thumb_up</i>' +
                        '<i class="material-icons">check</i>'
                )
            }
            else {
                $("#btn-like").html(
                    '<i class="material-icons">thumb_up</i>'
                )
            }
        }
    })
}

function addEditor(userId) {
    $.ajax({
        url: '/ajax/add-editor/',
        data: {
            'list_id': l_id,
            'user_id': userId
        },
        dataType: 'json'
    });

    // Remove from right column and add to left column
    var userRow = $("#user-" + userId);
    var userRowHtml = userRow.html();
    userRowHtml = userRowHtml.substring(85, userRowHtml.length - 42);
    console.log(userRowHtml);
    userRow.remove();
    $("#editor-list").append(
        '<tr id="user-' + userId + '">' +
        '<td>' + userRowHtml + '</td>' +
        '<td class="text-center">' +
        '<button type="button" class="btn btn-danger btn-simple btn-xs" onclick=\'removeEditor("' + userId + '", "' + userRowHtml + '")\'>' +
        '<i class="material-icons">close</i>' +
        '</button>' +
        '</td>' +
        '</tr>'
    );
}

function removeEditor(userId, text) {
    $.ajax({
        url: '/ajax/remove-editor/',
        data: {
            'list_id': l_id,
            'user_id': userId
        },
        dataType: 'json'
    });

    // Remove from left column and add to right column
    var userRow = $("#user-" + userId);
    userRow.remove();

    // Get first & last name combo
    var endIndex = text.indexOf('@') - 2;
    var name = text.substring(0, endIndex);
    console.log(name);

    $("#add-editor-list").append(
        '<tr class="pointer" onclick="addEditor(' + userId + ')" id="user-"' + userId + ' class="' + name + '">' +
        '<td><strong class="text-info"><</strong>' + text + '</td>' +
        '</tr>'
    );
}

function performDeletion() {
    window.location.href="delete/";
}

function deleteList() {
    functions.sweetAlert("warning-message-and-confirmation", "Are you sure you want to delete this list?",
        performDeletion);
}
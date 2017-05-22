$(document).ready(function() {
    $("#movie-input").keyup(function() {
        if ($(this).val().length > 2) {
            searchMovies();
        }
        else {
            destroyDropdown();
        }
    })
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
            "<li id='" + movies[i].id + "'><a>" + movies[i].title + "</a></li>"
        )
    }
}
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
            "<li id='" + movies[i].id + "' onclick='selectMovie(" + movies[i].id + ")'><a>" + movies[i].title + "</a></li>"
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
                addMovieRow(data);
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

function addMovieRow(movie) {
    var img_path = "../static/general/img/no_poster.jpg";
    if (movie.poster_path != null) {
        img_path = "http://image.tmdb.org/t/p/w92" + movie.poster_path;
    }
    $("#movie-table-body").append(
        "<tr onclick=window.location.href='/movie/" + movie.id + "/'>" +
            "<td>" +
                "<h4><img src='" + img_path +  "' alt=''>     " + movie.title + "</h4>" +
            "<td class='text-center'>" +
                "<h4>" + movie.release_date.substring(0, 4) + "</h4>" +
            "</td>" +
        "</tr>"
    );
}
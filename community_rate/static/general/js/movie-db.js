$(document).ready(function() {
    $("#filter-btn").click(function() {
        $("#movie-table-body").html('');
        var query = $("#filter-movies").val();
        filterMovies(query)
    });
});


function addMovieRow(index, movie) {
    var img_path = "../static/general/img/no_poster.jpg";
    if (movie.poster_path != null) {
        img_path = "http://image.tmdb.org/t/p/w92" + movie.poster_path;
    }
    $("#movie-table-body").append(
        "<tr onclick=window.location.href='/movie/" + movie.id + "/'>" +
            "<td>" +
                "<h4><img src='" + img_path +  "' alt=''>     " + movie.title + "</h4>" +
            "<td class='text-center' id='rating" + index + "'></td>" +
            "<td class='text-center'>" +
                "<h4>" + movie.release_date + "</h4>" +
            "</td>" +
        "</tr>"
    );
}

function addRatingToRow(index, rating) {
    var tagID = "#rating" + index;
    $(tagID).html(
        "<h4>" + rating + "</h4>"
    );
}

function filterMovies(query) {
    if (query.length > 2) {
        var index = 0;
        $.ajax({
            url: '/ajax/filter-movies/',
            data: {
                'query': query
            },
            dataType: 'json',
            success: function (data) {
                for (var i = 0; i < data.results.length; i++) {
                    addMovieRow(i, data.results[i]);
                    $.ajax({
                        url: '/ajax/get-movie-rating/',
                        data: {
                            'movie': data.results[i].id
                        },
                        dataType: 'json',
                        success: function(rating) {
                            addRatingToRow(index, rating.average_rating);
                            index++;
                        }
                    })
                }
            }
        })
    }
}
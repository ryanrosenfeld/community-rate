var prevEm = Null;
// $(document).ready(function() {
//     setImg({{ movie }})
// })

function showForm() {
    $("#rating-form").css("display", "block");
}

function hideForm() {
    $("#rating-form").css("display", "none");
}

function setReaction(em) {
    var s = "em " + "em-" + em;
    $("#reaction-field").val(s);
    $(prevEm).css("border", "none");
    var sel = ".em-" + em;
    $(sel).css("border", "solid #18BC9C 3px");
    $(sel).css("border-radius", "5px");
    prevEm = sel;
}

// function setImg(movie) {
//     var basePath = "http://image.tmdb.org/t/p/";
// 	var filePath = movie.poster_path;
// 	return basePath + 'w92' + filePath;
// }
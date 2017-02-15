// NAVBAR SEARCH
var apiKey = "fd8332d364611c30a611272eb023f170";

function search(str, success) {
	var settings = {
	  "async": true,
	  "crossDomain": true,
	  "url": "https://api.themoviedb.org/3/search/movie?api_key=" + apiKey + "&query=" + str,
	  "method": "GET",
	  "headers": {},
	  "data": "{}",
	  "success": success
	}

	$.ajax(settings).done(function(rsp) {
		return rsp;
	});
}

function searchById(id, success) {
	var settings = {
	  "async": true,
	  "crossDomain": true,
	  "url": "https://api.themoviedb.org/3/movie/" + id + "?language=en-US&api_key=fd8332d364611c30a611272eb023f170",
	  "method": "GET",
	  "headers": {},
	  "data": "{}",
	  "success": success
	}

	$.ajax(settings).done(function (rsp) {
	  return rsp;
	});
}

// Possible sizes: w92, w154, w185, w342, w500, w780, original
function getPosterImgSrc(movie, size) {
	var basePath = "http://image.tmdb.org/t/p/";
	var filePath = movie.poster_path;
	return basePath + size + filePath;
}

function postToURL(url, params) {
	var form = $('<form action="' + url + '" method="get" style="display:none">' +
	  '<input type="text" name="params" value="' + params + '" />' +
	  '</form>');
	$('body').append(form);
	form.submit();
}

// function postToURL(url, params) {
// 	var html = '<form action="' + url + '" method="get" style="display:none">';
// 	console.log(JSON.stringify(params));
// 	var keys = Object.keys(params);
// 	console.log(keys);
// 	for (var i = 0; i < keys.length; i++) {
// 		var key = keys[i];
// 		html += '<input type="text" name="' + key + '" value="' + params[i].key + '" />';
// 	}
//  	html += '</form>';
// 	var form = $(html);
// 	$('body').append(form);
// 	form.submit();
// }

function goToMovie(id) {
	postToURL("movie.html", id);
}

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1];
        }
    }
};

function checkForUser() {
	if (sessionStorage.getItem("currUser") != null) {
		return sessionStorage.getItem("currUser");
	}
	$.post("php/check-user.php", function(data) {
		if (data !== "false") {
			dataString = data;
			data = JSON.parse(data);
			sessionStorage.setItem("currUser", dataString);
			return data;
		}
		else {
			window.location.href = "login.html";
		}
	})
}

function addToListGroup(innerHTML, listID, action) {
	if (action == null) {
		action = "";
	}
	var html = "<button type='button' class='list-group-item list-group-item-action' " + action + ">" + innerHTML + "</button>";
	$("#" + listID).append(html);
}

// function showResult(str) {
// 	if (str.length == 0) {
// 		$("#livesearch").val("");
// 		return;
// 	}
// 	search(str, function(result) {

// 	})
// }

// AUTOCOMPLETE
// $('#autocomplete').autocomplete({
// 	lookup: function (query, done) {

// 	}
//     serviceUrl: baseURL + ,
//     onSelect: function (suggestion) {
//         alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
//     }
// });
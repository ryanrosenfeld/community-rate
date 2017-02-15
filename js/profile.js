function setUpPage() {
  $.post("php/get-reviews.php", function(data) {
    if (data.trim() !== "none") {
      reviews = jQuery.parseJSON(data);
      listFavorites();
      //listRecents();
      //showLists();
      getFriendships();
      $('#numSeen').append(reviews.length);
    }
  });
}

function listFavorites() {
  var sortedReviews = reviews;
  sortedReviews.sort(function(a,b) {
    return b.Rating - a.Rating;
  });
  listReviews(sortedReviews, "favoritesList");
  findFavorite(sortedReviews);
}

// function listRecents() {
//   var sortedReviews = reviews;
//   sortedReviews.sort(function(a,b) {
//     return b.dateReviewed - a.dateReviewed;
//   })
//   listReviews(sortedReviews, "recentsList");
// }

// function showLists() {
  
// }

function listReviews(list, divId) {
  for (var i = 0; i < list.length; i++) {
    var id = list[i].Movie_ID;
    searchById(id, function(rsp) {
      addToListGroup(rsp, divId);
      //var img = getPosterImgSrc(rsp, "w92");
    })
  }
}

function addToListGroup(movie, listId) {
  var html = "<button type='button' class='list-group-item list-group-item-action' onclick='goToMovie(" + movie.id + ")'>" + movie.title + "</button>";
  $("#" + listId).append(html);
}

function findFavorite(sortedReviews) {
  var id = sortedReviews[0].Movie_ID;
  searchById(id, function(rsp) {
    $('#favMovie').append(rsp.title);
  })
}

function getFriendships() {
  console.log("Here");
  $.post("php/get-friendships.php", function (rsp) {
    rsp = JSON.parse(rsp);
    console.log(rsp);
    var followers = rsp[0];
    var following = rsp[1];
  })
}








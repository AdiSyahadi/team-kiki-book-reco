// var api = 'http://openlibrary.org/search.json?q='

// function httpGet(theUrl)
// {
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
//     xmlHttp.send( null );
//     return xmlHttp.responseText;
// }

// var HttpClient = function() {
//     this.get = function(aUrl, aCallback) {
//         var anHttpRequest = new XMLHttpRequest();
//         anHttpRequest.onreadystatechange = function() { 
//             if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
//                 aCallback(anHttpRequest.responseText);
//         }

//         anHttpRequest.open( "GET", aUrl, true );            
//         anHttpRequest.send( null );
//     }
// }

// function search(){
//     // var query_result = httpGet(api+'harry+potter')
//     var client = new HttpClient();
//     client.get(api+'harry+potter', function(response) {
//         // do something with response
//         alert(response);
//     });
// }

// function init(){
//     document.getElementById('submit').addEventListener("click", search);
// }

// window.onload = init;
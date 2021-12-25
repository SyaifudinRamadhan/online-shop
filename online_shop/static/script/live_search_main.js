// var rows = document.getElementById('table').getElementsByTagName('tr');
function search(id, card_id){
	// Jalankan live get aearch keyword 
	var keyword  = document.getElementById(id).value;

	var filter, cards, body, title, i, txtValue;
		  // input = document.getElementById("myInput");
	filter = keyword.toUpperCase();
	cards = document.getElementById(card_id);
	body = cards.getElementsByClassName("card");
	// console.log(keyword)
		  // Loop through all table rows, and hide those who don't match the search query
	for (i = 0; i < body.length; i++) {
		title = body[i].getElementsByTagName("h5")[0];
		if (title) {
		   txtValue = title.textContent || title.innerText;
		   if (txtValue.toUpperCase().indexOf(filter) > -1) {
		        body[i].style.display = "";
		    } else {
		        body[i].style.display = "none";
		        console.log('loop'+String(i))
		    }
		  } 
		  console.log('cek load');
		}

	if (keyword == ''){
		window.location.reload();
	}

}


// var rows = document.getElementById('table').getElementsByTagName('tr');
// document.getElementById('search').addEventListener('keyup', function (){
// 	var keyword = trim(this.value.replace(/ +/g, ' ')).toLowerCase();
//     console.log(keyword);
    
//       rows.show().filter(function(){
//       	var text = this.text().replace(/\s+/g, ' ').toLowerCase();
//         return !~text.indexOf(keyword);
//       }).hide();
// });



// document.getElementById('Search2').addEventListener('keyup', function(){
// 	search('Search2', 1, 'data');
// });
// document.getElementById('Search3').addEventListener('keyup', function(){
// 	search('Search3', 2, 'data');
// });

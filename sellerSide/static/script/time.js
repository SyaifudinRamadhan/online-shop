function timeLoad(){
	const today = new Date();
	let h = today.getHours();
	let m = today.getMinutes();
	let s = today.getSeconds();

	document.getElementById("time").innerHTML = today;
	setTimeout(timeLoad, 1000);
}

function preventBack(){
	$(document).ready(function(){
		function disableBack(){
			window.history.forward();
		}
		window.onload = disableBack();
		window.onpageshow = function(evt){
			if (evt.presisted){ 
				disableBack();
			}
		}
	});

	timeLoad();
}

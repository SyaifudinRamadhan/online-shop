function get_snap(cls_token, cls_btn){
	let token = document.querySelectorAll(cls_token)[0].value;
	console.log(token);

	let checkoutBtn = document.querySelectorAll(cls_btn)[0];
	console.log(checkoutBtn);
	checkoutBtn.onclick = function(){
	console.log('opening snap popup:');
					        
			// Open Snap popup with defined callbacks.
	snap.pay(token, {
		onSuccess: function(result) {
			console.log("SUCCESS", result);
			alert("Payment accepted \r\n"+JSON.stringify(result));
			window.location.href='/oAuth/o_auth_order_pay';
		},
		onPending: function(result) {
			console.log("Payment pending", result);
			alert("Payment pending \r\n"+JSON.stringify(result));
			window.location.href='/oAuth/o_auth_order_pay';
		},
		onError: function() {
			console.log("Payment error");
		}
	});
					        // For more advanced use, refer to: https://snap-docs.midtrans.com/#snap-js
	};
}
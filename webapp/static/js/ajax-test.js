$(document).ready(function() {

	$('form').on('submit', function(event) {

		var mail = $("#email").val();
    	var pass = $("#password").val();

		event.preventDefault();

		var url_bg = '/login';
		var url_index = '/';

		$.ajax({
			type : 'POST',
			url : url_bg,
			contentType: "application/json; charset=utf-8",
			// contentType: "application/x-www-form-urlencoded",
            cache: false,
			dataType: "json",
			data : JSON.stringify({
				email: mail,
				password : pass,
			}),
			success: function(e){
		       console.log(e);
		   	},
		})
		.done(function(data) {

			$('#successAlert').text(data.name).show();
			window.location = url_index;

			// if (data.error) {
			// 	$('#errorAlert').text(data.error).show();
			// 	$('#successAlert').hide();
			// 	window.location = url_index;
			// }
			// else {
			// 	window.location = url_home;
			// 	$('#successAlert').text(data.name).show();
			// 	$('#errorAlert').hide();
			// }

		});
	});
});

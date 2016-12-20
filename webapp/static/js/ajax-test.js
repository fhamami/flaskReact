// $(document).ready(function() {
//
// 	$('form').on('submit', function(event) {
//
// 		var mail = $("#email").val();
//     	var pass = $("#password").val();
//
// 		event.preventDefault();
//
// 		var url_bg = '/login';
// 		var url_index = '/';
//
// 		$.ajaxSetup({
// 		    beforeSend: function(xhr, settings) {
// 		        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
// 		            xhr.setRequestHeader("X-CSRFToken", csrftoken)
// 		        }
// 		    }
// 		})
//
// 		$.ajax({
// 			type : 'POST',
// 			url : url_index,
// 			contentType: "application/json; charset=utf-8",
// 			// contentType: "application/x-www-form-urlencoded",
//             cache: false,
// 			dataType: "json",
// 			data : JSON.stringify({
// 				email: mail,
// 				password : pass,
// 			}),
// 			success: function(e){
// 		       console.log(e);
// 		   	},
// 		})
// 		.done(function(data) {
//
// 			$('#successAlert').text(data.name).show();
// 			console.log('done!')
// 			// window.location = url_index;
//
// 			// if (data.error) {
// 			// 	$('#errorAlert').text(data.error).show();
// 			// 	$('#successAlert').hide();
// 			// 	window.location = url_index;
// 			// }
// 			// else {
// 			// 	window.location = url_home;
// 			// 	$('#successAlert').text(data.name).show();
// 			// 	$('#errorAlert').hide();
// 			// }
//
// 		});
// 		ajax.fail(function(data){
// 			console.log('error!');
// 		});
// 	});
// });

function sendLoginAjax(evt){
	// lets make an ajax request.
	evt.preventDefault();

	var csrftoken = $('meta[name=csrf-token]').attr('content')

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken)
	        }
	    }
	})

	var usernameToSend = $("#email").val();
	var passwordToSend = $("#password").val();

	var postParams = {
		'email': usernameToSend,
		'password': passwordToSend
	};

	// AJAX
	$.post('/login.json', postParams, function(data){
		$('#loginform').remove();
		$('#dropdown').html('<div>Welcome</div>');
		$('#alert-section').html('<div class="alert alert-success" role="alert"> You are logged in.</div>');
		$('#logout-section').append('<button id="logout">Logout</button>');
	});
}

function logOut(evt){
	$.post('/logout.json', function(data){
		$('#alert-section').empty();
		$('#alert-section').html('<div class="alert alert-info" role="alert">Log out successful.</div>');
		$('#loginform').html('<form id="myform"><label>Username<input id="email" name="email" type="text"></label><label>Password<input id="password" name="password" type="password"></label><input id="submit-btn" type="submit" value="Log In"></form>');
		$('#logout').remove();
	});
}

// when the form submits, call this function
$('#submit-btn').on('click', sendLoginAjax);
// when the user clicks logout button, call this functions
$('#logout').on('click', logOut);

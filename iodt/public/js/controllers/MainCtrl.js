angular.module('MainCtrl', []).controller('MainCtrl', function($scope, $rootScope, $location) {

	$('#dob').datepicker({
		'autoclose': true,
	});

	$scope.loginButton = function() {
		$('#loginMsg').text('');
		$rootScope.usrId = $('#usrid').val();
		data = "user_name=" + $('#usrid').val();
		data += "&password=" + $('#pwd').val();
		$.ajax({
			type: "POST",
			url: '/api/users/login',
			data: data,
			contentType: 'application/x-www-form-urlencoded',
			success: function(response) {
				if(response["Error"] == false && response["Message"] == "Success") {
					$location.url("dashboard");
					$('#userNameDiv').text(response["Users"][0].name);
					$('#loginDiv').hide();
					$('#logoutDiv').show();
				} else {
					$('#loginMsg').text(response["Message"]);
				}
			}
		});
		$('#usrid').val('');
		$('#pwd').val('');
	}

	$scope.registerButton = function() {
		$('#registerMsg').text('');
		$rootScope.usrId = $('#usrid').val();

		var date = new Date($('#dob').val());
		var d = date.getDate();
		var m = (date.getMonth()) + 1;
		var y = date.getFullYear();
		var formattedDate = "" + y + "-" + m + "-" + d;

		data = "user_name=" + $('#usrid').val();
		data += "&name=" + $('#name').val();
		data += "&email=" + $('#email').val();
		data += "&password=" + $('#pwd').val();
		data += "&number=" + $('#number').val();
		data += "&gender=" + $('[name="gender"]').val();
		data += "&dob=" + formattedDate;//$('#dob').val();
		data += "&address=" + $('#address').val();
		$.ajax({
			type: "POST",
			url: '/api/users/register',
			data: data,
			contentType: 'application/x-www-form-urlencoded',
			success: function(response) {
				if(response["Error"] == false && response["Message"] == "Success") {
					$location.path("/dashboard");
					$('#userNameDiv').text(response["Users"][0].name);
					$('#loginDiv').hide();
					$('#logoutDiv').show();
				} else {
					$('#registerMsg').text(response["Message"]);
				}
			}
		});
	}

	$scope.cancel = function() {
		$location.path("/");
	}

	$scope.logOut = function() {
		$location.path("/");
		$rootScope.usrId = "";
		$('#userNameDiv').text('');
		$('#logoutDiv').hide();
		$('#loginDiv').show();
	}

});

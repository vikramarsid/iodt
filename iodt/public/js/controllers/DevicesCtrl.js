angular.module('DevicesCtrl', []).controller('DevicesCtrl', function($scope, $rootScope, $http, $location) {

	$http.get('/api/devices/user/' + "a")//$rootScope.usrId)
	.success(function(response) {
		if(response["Error"] == false && response["Message"] == "Success") {
			$scope.devices = response["Devices"];
		}
	});

	$scope.createDevice = function(createDeviceForm) {
		$('#createDeviceMsg').text('');
		var data = "device_id=" + createDeviceForm.device_id;
		data += "&name=" + createDeviceForm.name;
		data += "&enode=" + createDeviceForm.enode;
		data += "&host=" + createDeviceForm.host;
		data += "&description=" + createDeviceForm.description;
		data += "&power_usage=" + createDeviceForm.power_usage;
		data += "&priority=" + createDeviceForm.priority;
		data += "&status=" + "active"//$('#status').val();
		$scope.clearForm();
		$http({
			method: "POST",
			url: '/api/devices',
			data: data,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.devices.push(response["Devices"][0]);
				$('#new').modal('hide');
			} else {
				$('#createDeviceMsg').text(response["Message"]);
			}
		});
	}

	$scope.updateDevice = function(device) {
		$('#updateDeviceMsg').text('');
		$scope.editDeviceForm = jQuery.extend(true, {}, device);
	}

	$scope.doUpdateDevice = function(device) {
		$('#updateDeviceMsg').text('');
		var data = "device_id=" + device.device_id;
		data += "&name=" + device.name;
		data += "&enode=" + device.enode;
		data += "&host=" + device.host;
		data += "&description=" + device.description;
		data += "&power_usage=" + device.power_usage;
		data += "&priority=" + device.priority;
		data += "&status=" + "active"//$('#status').val();
		$http({
			method: "PUT",
			url: '/api/devices/' + device.device_id,
			data: data,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.devices.forEach(function(obj, i) {
					if(obj.device_id == response["Devices"][0].device_id) {
						$scope.devices[i] = response["Devices"][0];
					}
				});
				$('#edit').modal('hide');
			} else {
				$('#updateDeviceMsg').text(response["Message"]);
			}
		});
	}

	$scope.deleteDevice = function(device) {
		$('#deleteDeviceMsg').text("");
		$scope.deleteDeviceForm = device;
	}

	$scope.doDeleteDevice = function(device) {
		$scope.deleteDeviceForm = '';
		$('#deleteDeviceMsg').text('');
		$http({
			method: "DELETE",
			url: '/api/devices/' + device.device_id,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.devices = $scope.devices.filter(function(obj) {
					return obj.device_id !== device.device_id;
				});
				$('#delete').modal('hide');
			} else {
				$('#deleteDeviceMsg').text(response["Message"]);
			}
		});
	}

	$scope.clearForm = function() {
		$scope.createDeviceForm.device_id = '';
		$scope.createDeviceForm.name = '';
		$scope.createDeviceForm.enode = '';
		$scope.createDeviceForm.host = '';
		$scope.createDeviceForm.description = '';
		$scope.createDeviceForm.power_usage = '';
		$scope.createDeviceForm.priority = '';
		$scope.createDeviceForm.status = '';
	}

});

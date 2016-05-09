angular.module('ClustersCtrl', []).controller('ClustersCtrl', function($scope, $rootScope, $http, $location, $httpParamSerializer) {

	$scope.unassignedDevices = {};
	$scope.devicesOfSelectedCluster = [];
	$scope.clusters = [];


	$http.get('/api/clusters/user/' + "a")//$rootScope.usrId)
	.success(function(response) {
		if(response["Error"] == false && response["Message"] == "Success") {
			$scope.clusters = response["Clusters"];
		}
	});

	$scope.getUnassignedDevices = function() {
		$http.get('/api/iodt/availableDevices')
		.success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.unassignedDevices = response["Devices"];
			} else {
				$scope.unassignedDevices = {};
			}
		});
	}

	$scope.getUnassignedDevices();

	$scope.createCluster = function(createClusterForm) {
		$('#createClusterMsg').text('');
		var data = "cluster_id=" + createClusterForm.cluster_id;
		data += "&name=" + createClusterForm.name;
		data += "&description=" + createClusterForm.description;
		data += "&power_limit=" + createClusterForm.power_limit;

		if(createClusterForm.devices != undefined && Object.keys(createClusterForm.devices).length != 0) {
			var keys = Object.keys(createClusterForm.devices);
			for (var i=keys.length; i--;) {
				if(createClusterForm.devices[keys[i]] == false) {
					delete createClusterForm.devices[keys[i]];
				}
			}
			var deviceArray = Object.keys(createClusterForm.devices);
			for (var i in deviceArray) {
				data += "&device_id=" + deviceArray[i];
			}
		}

		$scope.clearForm();
		$http({
			method: "POST",
			url: '/api/clusters/user/' + "a",//$rootScope.usrId,
			data: data,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			$scope.getUnassignedDevices();
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.clusters.push(response["Clusters"][0]);
				$('#new').modal('hide');
			} else {
				$('#createClusterMsg').text(response["Message"]);
			}
		});
	}

	$scope.updateCluster = function(cluster) {
		$('#updateClusterMsg').text('');
		$scope.editClusterForm = jQuery.extend(true, {}, cluster);
	}

	$scope.doUpdateCluster = function(cluster) {
		$('#updateClusterMsg').text('');
		var data = "cluster_id=" + cluster.cluster_id;
		data += "&name=" + cluster.name;
		data += "&description=" + cluster.description;
		data += "&power_limit=" + cluster.power_limit;
		$http({
			method: "PUT",
			url: '/api/clusters/' + cluster.cluster_id,
			data: data,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.clusters.forEach(function(obj, i) {
					if(obj.cluster_id == response["Clusters"][0].cluster_id) {
						$scope.clusters[i] = response["Clusters"][0];
					}
				});
				$('#edit').modal('hide');
			} else {
				$('#updateClusterMsg').text(response["Message"]);
			}
		});
	}

	$scope.deleteCluster = function(cluster) {
		$('#deleteClusterMsg').text("");
		$scope.deleteClusterForm = cluster;
	}

	$scope.doDeleteCluster = function(cluster) {
		$scope.deleteClusterForm = '';
		$('#deleteClusterMsg').text('');
		$http({
			method: "DELETE",
			url: '/api/clusters/' + cluster.cluster_id,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.clusters = $scope.clusters.filter(function(obj) {
					return obj.cluster_id !== cluster.cluster_id;
				});
				$('#delete').modal('hide');
			} else {
				$('#deleteClusterMsg').text(response["Message"]);
			}
		});
	}

	$scope.clearForm = function() {
		$scope.createClusterForm.cluster_id = '';
		$scope.createClusterForm.name = '';
		$scope.createClusterForm.description = '';
		$scope.createClusterForm.power_limit = '';
		$scope.createClusterForm.devices = '';
	}

	$scope.loadDevices = function(cluster) {
		$scope.devicesOfSelectedCluster = [];
		$scope.selectedCluster = cluster.cluster_id;
		$http.get('/api/devices/cluster/' + cluster.cluster_id)
		.success(function(response) {
			if(response["Error"] == false && response["Message"] == "Success") {
				for(var device in response["Devices"]) {
					$scope.devicesOfSelectedCluster.push(response["Devices"][device]);
				}
			}
		});
	}

	$scope.addDevicesToCluster = function(addDevices) {
		$('#addDevicesMsg').text('');
		if(addDevices.devices != undefined && Object.keys(addDevices.devices).length != 0) {
			var keys = Object.keys(addDevices.devices);
			for (var i=keys.length; i--;) {
				if(addDevices.devices[keys[i]] == false) {
					delete addDevices.devices[keys[i]];
				}
			}
			var deviceArray = Object.keys(addDevices.devices);
			var data = "";
			for (var i in deviceArray) {
				if(data == "") {
					data = "device_id=" + deviceArray[i];
				} else {
					data += "&device_id=" + deviceArray[i];
				}
			}
			$http({
				method: "POST",
				url: '/api/iodt/addDevices/user/' + "a"/*$rootScope.usrId*/ + '/cluster/' + $scope.selectedCluster,
				data: data,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				}
			}).success(function(response) {
				$scope.getUnassignedDevices();
				if(response["Error"] == false && response["Message"] == "Success") {
					$('#addDevice').modal('hide');
					for(var device in response["Devices"]) {
						$scope.devicesOfSelectedCluster.push(response["Devices"][device]);
					}
				} else {
					$('#addDevicesMsg').text(response["Message"]);
				}
				$('#addDevice').modal('hide');
			});
		} else {
			$('#addDevicesMsg').text("You need to select atleast 1 device");
		}
		$scope.addDevices.devices = {};
	}

	$scope.removeDevice = function(device) {
		$('#removeDeviceMsg').text("");
		$scope.removeDeviceForm = device;
	}

	$scope.doRemoveDevice = function(device) {
		$scope.removeDeviceForm = '';
		$('#removeDeviceMsg').text('');
		$http({
			method: "DELETE",
			url: '/api/iodt/removeDevices/user/' + "a"/*$rootScope.usrId*/ + '/cluster/' + $scope.selectedCluster + '/device/' + device.device_id,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		}).success(function(response) {
			$scope.getUnassignedDevices();
			if(response["Error"] == false && response["Message"] == "Success") {
				$scope.devicesOfSelectedCluster = $scope.devicesOfSelectedCluster.filter(function(obj) {
					return obj.device_id !== device.device_id;
				});
				$('#removeDevice').modal('hide');
			} else {
				$('#removeDeviceMsg').text(response["Message"]);
			}
		});
	}

});

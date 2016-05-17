angular.module('DashboardCtrl', []).controller('DashboardCtrl', function($scope, $rootScope, $http, $location) {

	$http.get('/api/devices/user/' + "a")//$rootScope.usrId)
	.success(function(response) {
		$scope.totalDevices = 0;
		$scope.activeDevices = 0;
		$scope.inactiveDevices = 0;
		if(response["Error"] == false && response["Message"] == "Success") {
			$scope.totalDevices = response["Devices"].length;
			for(var device in response["Devices"]) {
				if(response["Devices"][device].status == "active") {
					$scope.activeDevices++;
				} else {
					$scope.inactiveDevices++;
				}
			}
			$scope.devices = response["Devices"];
		}
	});


	$http.get('/api/clusters/user/' + "a")//$rootScope.usrId)
	.success(function(response) {
		$scope.totalClusters = 0;
		if(response["Error"] == false && response["Message"] == "Success") {
			$scope.totalClusters = response["Clusters"].length;
			$scope.clusters = response["Clusters"];
		}
	});


	$http.get('/api/iodt/powerusage')
	.success(function(response) {
		var x = ['x'];
		var xdata = ['Power Usage'];
		for (var i = 0; i < response.length; i++) {
			x.push(new Date(response[i]["DATE"] + " " + response[i]["START TIME"]));
			xdata.push(response[i]["USAGE"]);
		};
		var chart = c3.generate({
			bindto: '#chart',
			data: {
				x: 'x',
				columns: [
					x, xdata,
				],
			},
			axis: {
				x: {
					type: 'timeseries',
					tick: {
						format: '%m/%d/%Y',
					}
				}
			}
		});
	});


});

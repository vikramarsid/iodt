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


});

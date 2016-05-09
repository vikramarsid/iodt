angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

	$routeProvider

	.when('/', {
		templateUrl: 'views/home.html',
		// controller: 'MainCtrl'
	})

	.when('/login', {
		templateUrl: 'views/login.html',
		// controller: 'MainCtrl'
	})

	.when('/logout', {
		templateUrl: 'views/home.html',
		// controller: 'MainCtrl'
	})

	.when('/register', {
		templateUrl: 'views/register.html',
		// controller: 'MainCtrl'
	})

	.when('/dashboard', {
		templateUrl: 'views/dashboard.html',
		controller: 'DashboardCtrl'
	})

	.when('/clusters', {
		templateUrl: 'views/clusters.html',
		controller: 'ClustersCtrl'
	})

	.when('/devices', {
		templateUrl: 'views/devices.html',
		controller: 'DevicesCtrl'
	})

	$locationProvider.html5Mode(false);

}]);

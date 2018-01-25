define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name releaseApp.controller:HeaderCtrl
     * @description
     * # HeaderCtrl
     * Controller of the releaseApp
     */
    angular.module('releaseApp.controllers.HeaderCtrl', [])
        .controller('HeaderCtrl', function ($scope,$cookies,$state,$http) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader();
            });

            $scope.Logout = function() {
                $cookies.remove('user');
                $http.get('/api/v2/logout');
                $state.go('/#/login');
            };
        });
});

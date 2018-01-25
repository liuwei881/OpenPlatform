define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name releaseApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the releaseApp
     */
    angular.module('releaseApp.controllers.DashboardCtrl', [])
        .controller('DashboardCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

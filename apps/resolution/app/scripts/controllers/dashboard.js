define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name resolutionApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the resolutionApp
     */
    angular.module('resolutionApp.controllers.DashboardCtrl', [])
        .controller('DashboardCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

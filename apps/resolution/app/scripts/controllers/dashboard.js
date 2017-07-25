define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.DashboardCtrl', [])
        .controller('DashboardCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

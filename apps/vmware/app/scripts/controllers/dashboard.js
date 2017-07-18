define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the kvmApp
     */
    angular.module('vmwareApp.controllers.DashboardCtrl', [])
        .controller('DashboardCtrl', function ($scope, $http, $cookies) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.initPage = function(){
                $scope.username = $cookies.get('username');
        };
            $scope.initPage();
            });
});


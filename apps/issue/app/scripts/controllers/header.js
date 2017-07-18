define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:HeaderCtrl
     * @description
     * # HeaderCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.HeaderCtrl', [])
        .controller('HeaderCtrl', function ($scope,$cookies,$state,$http) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader();
                $scope.initPage();
            });

            $scope.Logout = function() {
                $cookies.remove('user');
                $http.get('/api/v2/logout');
                $state.go('/#/login');
            };
        });
});

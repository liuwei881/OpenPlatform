define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:HeaderCtrl
     * @description
     * # HeaderCtrl
     * Controller of the kvmApp
     */
    angular.module('vmwareApp.controllers.HeaderCtrl', [])
        .controller('HeaderCtrl', function ($scope,$cookies,$state) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

            $scope.initPage = function(){
                $scope.username = $cookies.get('username');
        };

            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader();
                $scope.initPage();
            });

            $scope.Logout = function() {
                $cookies.remove('username');
                $state.go('login');
            };

        });
});

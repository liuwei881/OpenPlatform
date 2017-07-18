define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name portalApp.controller:HeaderCtrl
     * @description
     * # HeaderCtrl
     * Controller of the portalApp
     */
    angular.module('portalApp.controllers.HeaderCtrl', [])
        .controller('HeaderCtrl', function ($scope,$cookies,$state) {

            $scope.initPage = function(){
                $scope.username = $cookies.get('username');
            }
            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader();
                $scope.initPage();
            });
            $scope.Logout = function() {
                $cookies.remove('user');
                $cookies.remove('username');
                $state.go('login');
            };

        });
});

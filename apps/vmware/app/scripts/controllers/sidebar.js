define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kubernetesApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the kubernetesApp
     */
    angular.module('vmwareApp.controllers.SidebarCtrl', [])
        .controller('SidebarCtrl', function ($scope, $http) {

            $scope.$on('$includeContentLoaded', function () {
                Layout.initSidebar();
            });

            $scope.pageSidebarClosed= false;
        });
});

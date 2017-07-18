define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name portalApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the portalApp
     */
    angular.module('portalApp.controllers.SidebarCtrl', [])
        .controller('SidebarCtrl', function ($scope) {

            $scope.$on('$includeContentLoaded', function () {
                Layout.initSidebar();
            });

            $scope.pageSidebarClosed= false;
        });
});

define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name releaseApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the releaseApp
     */
    angular.module('releaseApp.controllers.SidebarCtrl', [])
        .controller('SidebarCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                //Layout.initSidebar();
            });
        });
});

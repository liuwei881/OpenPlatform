define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name resolutionApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the resolutionApp
     */
    angular.module('resolutionApp.controllers.SidebarCtrl', [])
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

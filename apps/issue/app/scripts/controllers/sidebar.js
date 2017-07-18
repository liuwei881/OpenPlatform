define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.SidebarCtrl', [])
        .controller('SidebarCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                Layout.initSidebar();
            });
        });
});

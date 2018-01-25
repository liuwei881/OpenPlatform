define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name releaseApp.controller:FooterCtrl
     * @description
     * # FooterCtrl
     * Controller of the releaseApp
     */
    angular.module('releaseApp.controllers.FooterCtrl', [])
        .controller('FooterCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                Layout.initFooter(); // init footer
            });
        });
});

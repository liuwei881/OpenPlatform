define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:FooterCtrl
     * @description
     * # FooterCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.FooterCtrl', [])
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

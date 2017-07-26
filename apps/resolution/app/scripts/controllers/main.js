define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name resolutionApp.controller:MainCtrl
     * @description
     * # MainCtrl
     * Controller of the resolutionApp
     */
    angular.module('resolutionApp.controllers.MainCtrl', [])
        .controller('MainCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

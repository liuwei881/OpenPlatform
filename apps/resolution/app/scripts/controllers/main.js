define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:MainCtrl
     * @description
     * # MainCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.MainCtrl', [])
        .controller('MainCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

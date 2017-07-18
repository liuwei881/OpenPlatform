define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:PageHeadCtrl
     * @description
     * # PageHeadCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.PageHeadCtrl', [])
        .controller('PageHeadCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

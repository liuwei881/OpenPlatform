define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name releaseApp.controller:PageHeadCtrl
     * @description
     * # PageHeadCtrl
     * Controller of the releaseApp
     */
    angular.module('releaseApp.controllers.PageHeadCtrl', [])
        .controller('PageHeadCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

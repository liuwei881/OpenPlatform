define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:PageHeadCtrl
     * @description
     * # PageHeadCtrl
     * Controller of the kubernetesApp
     */
    angular.module('vmwareApp.controllers.PageHeadCtrl', [])
        .controller('PageHeadCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});

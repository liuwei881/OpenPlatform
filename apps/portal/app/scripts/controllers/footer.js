define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name portalApp.controller:FooterCtrl
     * @description
     * # FooterCtrl
     * Controller of the portalApp
     */
    angular.module('portalApp.controllers.FooterCtrl', [])
        .controller('FooterCtrl', function ($scope) {
           
            $scope.$on('$includeContentLoaded', function () {
                Layout.initFooter(); // init footer
            });
        });
});

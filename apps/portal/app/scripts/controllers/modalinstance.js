define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name portalApp.controller:ModalInstanceCtrlCtrl
     * @description
     * # ModalInstanceCtrlCtrl
     * Controller of the portalApp
     */
    angular.module('portalApp.controllers.ModalInstanceCtrl', ['ui.bootstrap', 'ui.bootstrap.tpls'])
        .controller('ModalInstanceCtrl', function ($scope, $modalInstance, item, title) {
            
            $scope.item = item;
            $scope.title = title;
            $scope.Save = function (isValid) {
                $modalInstance.save($scope.item, isValid);
            };

            $scope.Delete = function () {
                $modalInstance.Delete($scope.item);
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
            $scope.diyfun = function (params) {
                $modalInstance.diyfun(params);
            };
        });
});

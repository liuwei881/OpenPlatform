define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name issueApp.controller:ModalInstanceCtrlCtrl
     * @description
     * # ModalInstanceCtrlCtrl
     * Controller of the issueApp
     */
    angular.module('issueApp.controllers.ModalInstanceCtrl', [])
        .controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, item, title) {
            this.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.item = item;
            $scope.title = title;
            $scope.Save = function () {
                $uibModalInstance.save($scope.item);
            };

            $scope.Update = function () {
                $uibModalInstance.Update($scope.item);
            };

            $scope.Updateapp = function () {
                $uibModalInstance.Updateapp($scope.item);
            };

            $scope.Delete = function () {
                $uibModalInstance.Delete($scope.item);
            };

            $scope.Start = function () {
                $uibModalInstance.Start($scope.item);
            };

            $scope.Stop = function () {
                $uibModalInstance.Stop($scope.item);
            };

            $scope.appdel = function () {
                $uibModalInstance.appdel($scope.item);
            };

            $scope.imagesave = function () {
                $uibModalInstance.imagesave($scope.item);
            };

            $scope.imagedel = function () {
                $uibModalInstance.imagedel($scope.item);
            };

            $scope.delimage = function () {
                $uibModalInstance.delimage($scope.item);
            };

            $scope.Startimage = function () {
                $uibModalInstance.Startimage($scope.item);
            };

            $scope.saveApp = function () {
                $uibModalInstance.saveApp($scope.item);
            };

            $scope.Updateimage = function () {
                $uibModalInstance.Updateimage($scope.item);
            };

            $scope.projectstop = function () {
                $uibModalInstance.projectstop($scope.item);
            };

            $scope.projectstart = function () {
                $uibModalInstance.projectstart($scope.item);
            };

            $scope.projectdel = function () {
                $uibModalInstance.projectdel($scope.item);
            };

            $scope.saveApp = function () {
                $uibModalInstance.saveApp($scope.item);
            };


            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        });
});

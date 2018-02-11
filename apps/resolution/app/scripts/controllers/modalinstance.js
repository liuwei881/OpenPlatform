define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name resolutionApp.controller:ModalInstanceCtrlCtrl
     * @description
     * # ModalInstanceCtrlCtrl
     * Controller of the resolutionApp
     */
    angular.module('resolutionApp.controllers.ModalInstanceCtrl', [])
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

            $scope.Delete = function () {
                $uibModalInstance.Delete($scope.item);
            };

            $scope.Edit = function () {
                $uibModalInstance.Edit($scope.item);
            };

            $scope.Test = function () {
                $uibModalInstance.Test($scope.item);
            };

            $scope.DelBox = function () {
                $uibModalInstance.DelBox($scope.item);
            }

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
            $scope.choices = [{id: '1', name: '1'}];

            $scope.addNewChoice = function() {
                var newItemNo = $scope.choices.length+1;
                $scope.choices.push({'id' : '' + newItemNo, 'name' : '' + newItemNo});
                };

            $scope.removeNewChoice = function() {
            var newItemNo = $scope.choices.length-1;
            if ( newItemNo !== 0 ) {
                $scope.choices.pop();
                }
            };

            $scope.showAddChoice = function(choice) {
            return choice.id === $scope.choices[$scope.choices.length-1].id;
            };

        });
});

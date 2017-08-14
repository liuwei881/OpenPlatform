define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name resolutionApp.controller:ImageServerCtrl
   * @description
   * # ImageServerCtrl
   * Controller of the resolutionApp
   */
  angular.module('resolutionApp.controllers.resolutionServerCtrl', ['ui.bootstrap'])
    .controller('resolutionServerCtrl', function ($scope, $state, $uibModal,Async,Sync) {
      this.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];

        $scope.total = 0;
        $scope.pageSize = 15;
        $scope.page = 1;
        $scope.searchKey = '';
        $scope.initPage = function(searchKey){
            Async.get('/api/v2/resolution',{page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows  = data.rows;
                    $scope.username = data.username;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
            var allZone = JSON.parse(Sync.fetch('/api/v2/zone/'));
            var recordtype = JSON.parse(Sync.fetch('/api/v2/recordtype/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'add.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return {};
                    },
                    title: function () {
                        return {'title':'新建解析', 'ZoneList':allZone, 'RecordType':recordtype};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                Async.save('/api/v2/resolution/',item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Delete = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'delete.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'删除解析'};
                    }
                }
            });
           modalInstance.Delete = function (item) {
                Async.Delete('/api/v2/resolution/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Edit = function (i) {
            var allZone = JSON.parse(Sync.fetch('/api/v2/zone/'));
            var recordtype = JSON.parse(Sync.fetch('/api/v2/recordtype/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'edit.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'修改解析', 'ZoneList':allZone, 'RecordType':recordtype};
                    }
                }
            });
           modalInstance.Edit = function (item) {
                Async.Edit('/api/v2/resolution/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };


        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.pageAction = function (page) {
            Async.get('/api/v2/resolution/',{page: page})
                .success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

    });
});

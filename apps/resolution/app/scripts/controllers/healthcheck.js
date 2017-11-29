define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name resolutionApp.controller:ImageServerCtrl
   * @description
   * # ImageServerCtrl
   * Controller of the resolutionApp
   */
  angular.module('resolutionApp.controllers.healthcheckCtrl', ['ui.bootstrap'])
    .controller('healthcheckCtrl', function ($scope, $state, $uibModal,Async,Sync) {
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
            Async.get('/api/v2/healthcheck',{page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows  = data.rows;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
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
                        return {'title':'新建健康检查'};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                Async.save('/api/v2/healthcheck/',item).
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
                        return {'title':'删除健康检查'};
                    }
                }
            });
           modalInstance.Delete = function (item) {
                Async.Delete('/api/v2/healthcheck/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Edit = function (i) {
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
                        return {'title':'修改解析','RecordType':recordtype};
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

        $scope.Test = function (i) {
            var digtest = Sync.fetch('/api/v2/digtest/' + $scope.rows[i].Id);
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'test.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'dig测试', 'digtest': digtest};
                    }
                }
            });
        };

        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.pageAction = function (page, searchKey) {
            Async.get('/api/v2/resolution/',{page: page, pageSize: $scope.pageSize, searchKey:searchKey})
                .success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

    });
});

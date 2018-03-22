define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kvmApp.controller:ProjectServerCtrl
   * @description
   * # ProjectServerCtrl
   * Controller of the kubernetesApp
   */
  angular.module('vmwareApp.controllers.VmServerCtrl', [])
    .controller('VmServerCtrl', function ($scope, $state, $uibModal,Async,Sync) {
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
            Async.get('/api/v2/vms',{page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                    $scope.username = data.username;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
            var allImage = JSON.parse(Sync.fetch('/api/v2/mirror/'));
            var datacenter = JSON.parse(Sync.fetch('/api/v2/datacenter/'));
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
                        return {'title':'新建','imageList':allImage,'datacenter':datacenter};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                Async.save('/api/v2/vms',item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.edit = function (i) {
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
                        return {'title':'编辑'};
                    }
                }
            });
           modalInstance.vmsput = function (item) {
                Async.vmsput('/api/v2/vms',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Stop = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'stop.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'关闭虚拟机'};
                    }
                }
            });
           modalInstance.Stop = function (item) {
                Async.Stop('/api/v2/vms/stop/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                    });
            };
        };

        $scope.Restart = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'restart.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'重启虚拟机'};
                    }
                }
            });
           modalInstance.Restart = function (item) {
                Async.Restart('/api/v2/vms/restart/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
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
                        return {'title':'删除虚拟机'};
                    }
                }
            });
           modalInstance.Delete = function (item) {
                Async.Delete('/api/v2/vms/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.MigrateVm = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'migratevm.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'迁移虚拟机'};
                    }
                }
            });
           modalInstance.MigrateVm = function (item) {
                Async.MigrateVm('/api/v2/vms/migratevm/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.CheckOrder = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'checkorder.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'查看工单'};
                    }
                }
            });
        };

        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.pageAction = function (page) {
            Async.get('/api/v2/vms',{page: page}).success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };
    });
});

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
    .controller('resolutionServerCtrl', function ($scope, $state, $uibModal, $http, Async, Sync) {
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

        $scope.Select = function (i) {
            Async.get('/api/v2/status/' + $scope.rows[i].Id).success(function (data) {
                $scope.status = data.rows;
                var item = $scope.status;
                Async.Edit('/api/v2/status/', item).
                    success(function (data) {
                    console.log(item);
                 });

            });
        };

        $scope.All = function () {
            Async.get('/api/v2/status',{page: $scope.page, pageSize: $scope.pageSize}).
                success(function (data) {
                    $scope.status = data.rows;
                    var item = $scope.status;
                    for(var i=0;i<$scope.status.length;i++){
                        Async.Edit('/api/v2/status/', item[i]).
                        success(function (data) {
                        console.log(item);
                    });
                   }
                })
            };

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
                    },
                    choices: function () {
                        return {};
                    },
                    addNewChoice: function () {
                        return {};
                    },
                    removeNewChoice: function () {
                        return {};
                    },
                    showAddChoice: function () {
                        return {}
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

        $scope.DelBox = function () {
            var allName = JSON.parse(Sync.fetch('/api/v2/resolv/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'delbox.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return {}
                    },
                    title: function () {
                        return {'title':'批量删除解析', 'allName':allName};
                    }
                }
            });
           modalInstance.DelBox = function (item) {
                Async.get('/api/v2/resolv/').
                    success(function (data) {
                    $scope.all = data.all;
                    var item = $scope.all
                    for(var i=0;i<item.length;i++){
                        Async.Delete('/api/v2/resolution/',item[i]).
                        success(function (data) {
                        console.log(item);
                        modalInstance.close();
                    });
                };
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

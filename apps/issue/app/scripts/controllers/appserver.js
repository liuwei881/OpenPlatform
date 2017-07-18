define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kubernetesApp.controller:ImageServerCtrl
   * @description
   * # ImageServerCtrl
   * Controller of the kubernetesApp
   */
  angular.module('kubernetesApp.controllers.AppServerCtrl', ['ui.bootstrap'])
    .controller('AppServerCtrl', function ($scope, $state, $uibModal,Async,Sync) {
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
            Async.get('/api/v2/app',{page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
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
                        return {'title':'新建'};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                Async.save('/api/v2/app/',item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.detail = function (i) {
            $uibModal.open({
                animation: true,
                templateUrl: 'detail.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return '查看';
                    }
                }
            });
        };

        $scope.updateimage = function (i) {
            var allImage = JSON.parse(Sync.fetch('/api/v2/k8smirror/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'updateimage.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'升级镜像','imageList':allImage};
                    }
                }
            });
            modalInstance.Updateapp = function (item) {console.log(item);
                Async.Updateapp('/api/v2/updateapp/',item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.appdetail = function (i) {
            $uibModal.open({
                animation: true,
                templateUrl: 'appdetail.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return '查看应用信息';
                    }
                }
            });
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
           modalInstance.save = function (item) {
                Async.save('/api/v2/app/',item).
                    success(function (data) {
                    console.log(item);
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
                        return {'title':'删除'};
                    }
                }
            });
           modalInstance.appdel = function (item) {
                Async.appdel('/api/v2/app/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Start = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'start.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'启动应用'};
                    }
                }
            });
           modalInstance.Start = function (item) {
                Async.Start('/api/v2/start/',item).
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
                        return {'title':'停止应用'};
                    }
                }
            });
           modalInstance.Stop = function (item) {
                Async.Stop('/api/v2/stop/',item).
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
            Async.get('/api/v2/app/',{page: page})
                .success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

        $scope.sendReq = function(id, val){
         Async.post('/api/v2/app/rc/' + id, {"rc": val}).then(function(result){
            result.data;
         });
        };

    });
});

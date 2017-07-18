define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kubernetesApp.controller:ImageServerCtrl
   * @description
   * # ImageServerCtrl
   * Controller of the kubernetesApp
   */
  angular.module('kubernetesApp.controllers.ImageServerCtrl', ['ui.bootstrap'])
    .controller('ImageServerCtrl', function ($scope, $state, $cookies, $uibModal,Async,Sync) {
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
            Async.get('/api/v2/image',{page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows  = data.rows;
                    $scope.username = $cookies.get('username');
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

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
           modalInstance.imagesave = function (item) {
                Async.imagesave('/api/v2/image/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.addApp = function (ImageId) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'views/server/addApp.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return {'ImageId':ImageId};
                    },
                    title: function () {
                        return {'title':'创建应用'};
                    }
                }
            });
            modalInstance.saveApp = function (item) {
                Async.saveApp('/api/v2/app/',item).
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
                        return {'title':'删除'};
                    }
                }
            });
           modalInstance.imagedel = function (item) {
                Async.imagedel('/api/v2/image/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.delimage = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'delimage.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'删除镜像'};
                    }
                }
            });
           modalInstance.delimage = function (item) {
                Async.delimage('/api/v2/delimage/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.downimage = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'downimage.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'下载镜像'};
                    }
                }
            });
        };


        $scope.Start = function (item) {
             Async.Startimage('/api/v2/image/',item).
                success(function (data) {
                   console.log(item);
                     $scope.initPage();
                });
        };

        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.Openimage = function (ImageId) {
             Async.openimage('/api/v2/openimage/' + ImageId).
             success(function (data) {
                   console.log(ImageId);
                     $scope.initPage();
                });
        };

        $scope.Stopimage = function (ImageId) {
             Async.stopimage('/api/v2/stopimage/' + ImageId).
             success(function (data) {
                   console.log(ImageId);
                     $scope.initPage();
                });
        };

        $scope.pageAction = function (page) {
            Async.get('/api/v2/image/',{page: page})
                .success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

    });
});

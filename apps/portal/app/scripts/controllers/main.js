define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name portalApp.controller:MainCtrl
   * @description
   * # MainCtrl
   * Controller of the portalApp
   */
  angular.module('portalApp.controllers.MainCtrl', [])
    .controller('MainCtrl', function ($scope, Async) {
        this._AuthorCompany_ = 'Ciprun';

        $scope.initPage = function(){
            Async.get('/api/v2/protal').
                success(function (data) {
                    $scope.apps = data.rows;
                });
        };
        $scope.initPage();
    });
});

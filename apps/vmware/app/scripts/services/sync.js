define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name vmwareApp.TaskService
   * @description
   * # TaskService
   * Service in the vmwareApp.
   */
  angular.module('vmwareApp.services.Sync', [])
	.service('Sync', function ($http) {
        function fetch(url) {
            var request;
            if (window.XMLHttpRequest) {
                request = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
                request = new ActiveXObject("Microsoft.XMLHTTP");
            } else {
                throw new Error("Your browser don't support XMLHttpRequest");
            }
            request.open('GET', url, false);
            request.send(null);

            if (request.status === 200) {
                return request.responseText;
            }
        }

        function ShowSnap(url, KvmId) {
            return $http.get(url + KvmId)
        }

        function showdisksnap(url, SnapId){
            return $http.get(url + SnapId)
        }

        function showmember(url, ProjectId) {
            return $http.get(url + ProjectId);
        }

        return {
            fetch: fetch,
            ShowSnap: ShowSnap,
            showdisksnap: showdisksnap,
            showmember: showmember
        }
	});
});


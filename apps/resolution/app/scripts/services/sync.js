define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name issueApp.TaskService
   * @description
   * # TaskService
   * Service in the issueApp.
   */
  angular.module('issueApp.services.Sync', [])
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

        function showroleright(url, RoleId) {
            return $http.get(url + RoleId)
        }

        function showuserrole(url, RoleId) {
            return $http.get(url + RoleId)
        }

        return {
            fetch: fetch,
            showroleright: showroleright,
            showuserrole: showuserrole
        }
	});
});


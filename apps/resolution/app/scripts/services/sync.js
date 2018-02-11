define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name resolutionApp.TaskService
   * @description
   * # TaskService
   * Service in the resolutionApp.
   */
  angular.module('resolutionApp.services.Sync', [])
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

        function showresolv(url) {
            return $http.get(url)
        }

        return {
            fetch: fetch,
            showresolv: showresolv
        }
	});
});


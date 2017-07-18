define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name portalApp.Async
   * @description
   * # Async
   * Service in the portalApp.
   */
  angular.module('portalApp.services.Async', [])
	.service('Async', function ($http) {
	// AngularJS will instantiate a singleton by calling "new" on this function
	    function get(url, params){
            return $http.get(url, {params: params})
        }

        function save(url, params) {
            var urlArr = url.split('/');
            var len = urlArr.length;
            if (!isNaN(parseInt(urlArr[len-1])) && parseInt(urlArr[len-1]) != NaN) {
                return $http.put(url, {params: params});
            } else {
                return $http.post(url, {params: params});
            }
        }

        function del(url) {
            return $http.delete(url, {params: params});
        }

        return {
            get : get,
            save  : save,
            del   : del
        }
	});
});

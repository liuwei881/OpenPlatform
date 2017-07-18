define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kubernetesApp.Async
   * @description
   * # Async
   * Service in the kubernetesApp.
   */
  angular.module('kubernetesApp.services.Async', [])
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

        function Updateapp(url, params) {
            if (params.AppId != undefined) {
                return $http.put(url + params.AppId, {params: params})
            } else {
                return $http.post(url, {params: params})
            }
        }

        function imagesave(url, params) {
            if (params.ImageId != undefined) {
                return $http.put(url + params.ImageId, {params: params})
            } else {
                return $http.post(url, {params: params})
            }
        }

        function saveApp(url, params) {
            return $http.post(url,{params:params})
        }

        function Start(url, params) {
            return $http.get(url + params.AppId);
        }

        function Stop(url, params) {
            return $http.get(url + params.AppId);
        }

        function appdel(url, params) {
            return $http.delete(url + params.AppId);
        }

        function imagedel(params) {
            return $http.delete(url + params.ImageId);
        }

        function delimage(url,params) {
            return $http.get(url + params.ImageId);
        }

        function Startimage(params) {
            return $http.get(url + params.ImageId);
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        function Updateimage(url, params) {
            return $http.post(url + params.ProjectId,{params: params});
        }

        function projectsave(url, params) {
            if (params.ProjectName === undefined) {
                return $http.post(url)
            } else {
                return $http.post(url, {params: params})
            }
        }

        function projectdel(url, params) {
            return $http.delete(url + params.ProjectId);
        }

        function projectstart(url, params) {
            return $http.get(url + params.ProjectId);
        }

        function projectstop(url, params) {
            return $http.get(url + params.ProjectId);
        }

        function openimage(url) {
            return $http.get(url);
        }

        function stopimage(url) {
            return $http.get(url);
        }

        return {
            get : get,
            save : save,
            Updateapp : Updateapp,
            Start : Start,
            Stop:Stop,
            saveApp:saveApp,
            imagesave:imagesave,
            Startimage:Startimage,
            appdel: appdel,
            delimage: delimage,
            Updateimage: Updateimage,
            projectsave: projectsave,
            projectdel: projectdel,
            projectstart: projectstart,
            projectstop: projectstop,
            post : post,
            openimage: openimage,
            stopimage: stopimage
        }
	});
});

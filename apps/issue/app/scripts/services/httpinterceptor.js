define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc service
     * @name issueApp.httpInterceptor
     * @description
     * # httpInterceptor
     * Factory in the issueApp.
     */
    angular.module('issueApp.services.HttpInterceptor', [])
        .factory('httpInterceptor', function ($q, $rootScope, $cookies) {
            // Service logic
            // ...
            var meaningOfLife = 42;
            var apiUrl = '/api/v2';
            var shouldPrependApiUrl = function(reqConfig){
                if (!apiUrl) return false;
                return !(/[\s\S]*.html/.test(reqConfig.url) ||
                         (reqConfig.url && reqConfig.url.indexOf(apiUrl) === 0));
            }
            // Public API here
            return {
                someMethod: function () {
                    return meaningOfLife;
                },
                request: function (config) {
                    config.headers['X-Xsrftoken'] = $cookies.get('_xsrf');
                    if(apiUrl && shouldPrependApiUrl(config)){
                        config.url = apiUrl + config.url;
                    }
                    return config;
                },
                response: function (response) {
                    return response || $q.when(response);
                },
                responseError: function (rejection) {
                    if (rejection.status === 401) {
                        $rootScope.$state.go('login');
                    }
                    return $q.reject(rejection);
                }
            };
        });
});

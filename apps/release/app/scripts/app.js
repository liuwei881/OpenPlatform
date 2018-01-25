/*jshint unused: vars */
define(['angular', 'controllers/main', 'controllers/about', 'directives/paging', 'controllers/login', 'controllers/header', 'controllers/sidebar', 'controllers/pagehead', 'controllers/footer', 'controllers/dashboard', 'services/httpinterceptor', 'controllers/modalinstance', 'controllers/releaseserver', 'controllers/readyreleaseserver', 'controllers/tcpreleaseserver', 'services/async', 'services/sync']/*deps*/, function (angular, MainCtrl, AboutCtrl, PagingDirective, LoginCtrl, HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, DashboardCtrl, PhysicalCtrl, HttpInterceptorFactory, PhysicalService,  ModalinstanceCtrl, ReleaseServerCtrl, ReadyReleaseServerCtrl, TcpReleaseServerCtrl)/*invoke*/ {
    'use strict';

    /**
     * @ngdoc overview
     * @name releaseApp
     * @description
     * # releaseApp
     *
     * Main module of the application.
     */
    return angular
        .module('releaseApp', ['releaseApp.controllers.MainCtrl',
            'releaseApp.controllers.AboutCtrl',
            'releaseApp.directives.Paging',
            'releaseApp.controllers.LoginCtrl',
            'releaseApp.controllers.HeaderCtrl',
            'releaseApp.controllers.SidebarCtrl',
            'releaseApp.controllers.PageHeadCtrl',
            'releaseApp.controllers.FooterCtrl',
            'releaseApp.controllers.DashboardCtrl',
            'releaseApp.services.HttpInterceptor',
            'releaseApp.controllers.ModalInstanceCtrl',
            'releaseApp.controllers.ReleaseServerCtrl',
            'releaseApp.controllers.ReadyReleaseServerCtrl',
            'releaseApp.controllers.TcpReleaseServerCtrl',
            'releaseApp.services.Async',
            'releaseApp.services.Sync',
/*angJSDeps*/
            'ngCookies',
            'ngSanitize',
            'ngAnimate',
            'ui.router'
        ])
        .config(function ($stateProvider, $urlRouterProvider, $httpProvider) {
            $httpProvider.interceptors.push('httpInterceptor');
            $stateProvider
                .state('dashboard', {
                    url: '/',
                    templateUrl: 'views/main.html',
                    nav: 'DashHome'
                })
                .state('dashboard.home', {
                    url: '/dashboard',
                    templateUrl: 'views/dashboard.html',
                    controller: 'DashboardCtrl',
                    nav: 'DashBoard'
                })
                .state('dashboard.release', {
                    url: 'release',
                    templateUrl: 'views/release.html',
                    controller: 'ReleaseServerCtrl',
                    nav: '生产发布列表',
                    needRequest: true
                })
                .state('dashboard.readyrelease', {
                    url: 'readyrelease',
                    templateUrl: 'views/readyrelease.html',
                    controller: 'ReadyReleaseServerCtrl',
                    nav: '预生产发布列表',
                    needRequest: true
                })
                .state('dashboard.tcprelease', {
                    url: 'tcprelease',
                    templateUrl: 'views/tcprelease.html',
                    controller: 'TcpReleaseServerCtrl',
                    nav: 'TCP服务发布列表',
                    needRequest: true
                })
                .state('login',{
                    url: '/login',
                    templateUrl: 'views/login.html',
                    controller: 'LoginCtrl'
                })
                .state('logout',{
                    url: '/logout',
                    controller: function($cookies,$state){
                        $cookies.remove('user');
                        $state.go('login');
                    }
                })
            $urlRouterProvider.otherwise('/');
        })
        .run(function ($rootScope, $state, $stateParams, $cookies) {
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
            $rootScope.$on('$stateChangeStart', function (event, toState, fromState) {
                if (toState.url === '/login') {
                    $('body').addClass('login');
                } else {
                    $('body').removeClass('login');
                    if ($cookies.get('user') === undefined) {
                        event.preventDefault();
                        $state.go('login');
                    }
                }
            });
        });
    ;
});

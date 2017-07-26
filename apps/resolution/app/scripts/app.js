/*jshint unused: vars */
define(['angular', 'controllers/main', 'controllers/about', 'directives/paging', 'controllers/login', 'controllers/header', 'controllers/sidebar', 'controllers/pagehead', 'controllers/footer', 'controllers/dashboard', 'services/httpinterceptor', 'controllers/modalinstance', 'controllers/resolutionserver', 'services/async', 'services/sync']/*deps*/, function (angular, MainCtrl, AboutCtrl, PagingDirective, LoginCtrl, HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, DashboardCtrl, PhysicalCtrl, HttpInterceptorFactory, PhysicalService,  ModalinstanceCtrl, resolutionServerCtrl)/*invoke*/ {
    'use strict';

    /**
     * @ngdoc overview
     * @name resolutionApp
     * @description
     * # resolutionApp
     *
     * Main module of the application.
     */
    return angular
        .module('resolutionApp', ['resolutionApp.controllers.MainCtrl',
            'resolutionApp.controllers.AboutCtrl',
            'resolutionApp.directives.Paging',
            'resolutionApp.controllers.LoginCtrl',
            'resolutionApp.controllers.HeaderCtrl',
            'resolutionApp.controllers.SidebarCtrl',
            'resolutionApp.controllers.PageHeadCtrl',
            'resolutionApp.controllers.FooterCtrl',
            'resolutionApp.controllers.DashboardCtrl',
            'resolutionApp.services.HttpInterceptor',
            'resolutionApp.controllers.ModalInstanceCtrl',
            'resolutionApp.controllers.resolutionServerCtrl',
            'resolutionApp.services.Async',
            'resolutionApp.services.Sync',
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
                .state('dashboard.resolution', {
                    url: 'resolution',
                    templateUrl: 'views/resolution.html',
                    controller: 'resolutionServerCtrl',
                    nav: '解析列表',
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

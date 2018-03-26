/*jshint unused: vars */
define(['angular', 'controllers/main', 'controllers/about', 'directives/paging', 'controllers/login', 'controllers/header', 'controllers/sidebar', 'controllers/pagehead', 'controllers/footer', 'controllers/dashboard','services/httpinterceptor', 'controllers/modalinstance', 'controllers/assetserver','controllers/vmserver','services/async', 'services/sync',]/*deps*/, function (angular, MainCtrl, AboutCtrl, PagingDirective, LoginCtrl, HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, DashboardCtrl, PhysicalCtrl, HttpInterceptorFactory, PhysicalService, ModalinstanceCtrl, AssetServerCtrl,VmServerCtrl,SafetyServerCtrl,CloudDiskServerCtrl,ProjectServerCtrl,ShowSnapServerCtrl)/*invoke*/ {
    'use strict';

    /**
     * @ngdoc overview
     * @name vmwareApp
     * @description
     * # vmwareApp
     *
     * Main module of the application.
     */
    return angular
        .module('vmwareApp', ['vmwareApp.controllers.MainCtrl',
            'vmwareApp.controllers.AboutCtrl',
            'vmwareApp.directives.Paging',
            'vmwareApp.controllers.LoginCtrl',
            'vmwareApp.controllers.HeaderCtrl',
            'vmwareApp.controllers.SidebarCtrl',
            'vmwareApp.controllers.PageHeadCtrl',
            'vmwareApp.controllers.FooterCtrl',
            'vmwareApp.controllers.DashboardCtrl',
            'vmwareApp.services.HttpInterceptor',
            'vmwareApp.controllers.ModalInstanceCtrl',
            'vmwareApp.controllers.AssetServerCtrl',
            'vmwareApp.controllers.VmServerCtrl',
            'vmwareApp.services.Async',
            'vmwareApp.services.Sync',

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
                    url: 'dashboard',
                    templateUrl: 'views/dashboard.html',
                    controller: 'DashboardCtrl',
                    nav: 'DashBoard',
                    needRequest: true
                })
                .state('dashboard.vm', {
                    url: 'vms',
                    templateUrl: 'views/vm.html',
                    controller: 'VmServerCtrl',
                    nav: '虚拟机管理',
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
            $urlRouterProvider.otherwise('/login');
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

});

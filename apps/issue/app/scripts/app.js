/*jshint unused: vars */
define(['angular', 'controllers/main', 'controllers/about', 'directives/paging', 'controllers/login', 'controllers/header', 'controllers/sidebar', 'controllers/pagehead', 'controllers/footer', 'controllers/dashboard', 'services/httpinterceptor', 'controllers/modalinstance', 'controllers/issueserver', 'controllers/readyissueserver', 'services/async', 'services/sync']/*deps*/, function (angular, MainCtrl, AboutCtrl, PagingDirective, LoginCtrl, HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, DashboardCtrl, PhysicalCtrl, HttpInterceptorFactory, PhysicalService,  ModalinstanceCtrl, IssueServerCtrl, ReadyIssueServerCtrl)/*invoke*/ {
    'use strict';

    /**
     * @ngdoc overview
     * @name issueApp
     * @description
     * # issueApp
     *
     * Main module of the application.
     */
    return angular
        .module('issueApp', ['issueApp.controllers.MainCtrl',
            'issueApp.controllers.AboutCtrl',
            'issueApp.directives.Paging',
            'issueApp.controllers.LoginCtrl',
            'issueApp.controllers.HeaderCtrl',
            'issueApp.controllers.SidebarCtrl',
            'issueApp.controllers.PageHeadCtrl',
            'issueApp.controllers.FooterCtrl',
            'issueApp.controllers.DashboardCtrl',
            'issueApp.services.HttpInterceptor',
            'issueApp.controllers.ModalInstanceCtrl',
            'issueApp.controllers.IssueServerCtrl',
            'issueApp.controllers.ReadyIssueServerCtrl',
            'issueApp.services.Async',
            'issueApp.services.Sync',
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
                .state('dashboard.issue', {
                    url: 'issue',
                    templateUrl: 'views/issue.html',
                    controller: 'IssueServerCtrl',
                    nav: '生产发布列表',
                    needRequest: true
                })
                .state('dashboard.readyissue', {
                    url: 'readyissue',
                    templateUrl: 'views/readyissue.html',
                    controller: 'ReadyIssueServerCtrl',
                    nav: '预生产发布列表',
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

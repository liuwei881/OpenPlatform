/*jshint unused: vars */

define(['angular', 'controllers/main', 'directives/paging', 'controllers/login', 'controllers/header', 'controllers/sidebar', 'controllers/pagehead', 'controllers/footer', 'services/httpinterceptor', 'controllers/modalinstance', 'services/async', 'directives/ngspinnerbar']/*deps*/, function (angular, MainCtrl, PagingDirective, LoginCtrl, HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, HttpInterceptorFactory, ModalinstanceCtrl, Syncservice, NgSpinnerBarDirective)/*invoke*/ {

  'use strict';

  /**
   * @ngdoc overview
   * @name portalApp
   * @description
   * # portalApp
   *
   * Main module of the application.
   */
  return angular
       .module('portalApp', ['portalApp.controllers.MainCtrl',
       'portalApp.directives.Paging',
       'portalApp.controllers.LoginCtrl',
       'portalApp.controllers.HeaderCtrl',
       'portalApp.controllers.SidebarCtrl',
       'portalApp.controllers.PageHeadCtrl',
       'portalApp.controllers.FooterCtrl',
       'portalApp.services.HttpInterceptor',
       'portalApp.controllers.ModalInstanceCtrl',
       'portalApp.services.Async',
       'portalApp.directives.NgSpinnerBar',
       /*angJSDeps*/'ngCookies','ngResource','ngSanitize','ui.router'])
    .config(function ($stateProvider, $urlRouterProvider) {
       // $httpProvider.interceptors.push('httpInterceptor');
        $stateProvider
            .state('dashboard', {
                url: '/',
                templateUrl: 'views/main.html',
                controller: 'MainCtrl'
            })
            .state('login', {
                url: '/login',
                templateUrl: 'views/login.html',
                controller: 'LoginCtrl'
            })
     $urlRouterProvider.otherwise('/');
    })
    .run(function ($rootScope, $state, $stateParams, $cookies) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.$on('$stateChangeStart', function (event, toState, fromState) {
            if (toState.url === '/login') {
                $('body').addClass('login');
            }
            else {
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

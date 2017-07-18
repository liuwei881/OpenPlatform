/*jshint unused: vars */
require.config({
  paths: {
    angular: '../../asserts/angular/angular',
    'angular-cookies': '../../asserts/angular-cookies/angular-cookies',
    'angular-sanitize': '../../asserts/angular-sanitize/angular-sanitize',
    'angular-resource': '../../asserts/angular-resource/angular-resource',
    'angular-animate': '../../asserts/angular-animate/angular-animate',
    'angular-ui-router': '../../asserts/angular-ui-router/release/angular-ui-router',
    bootstrap: '../../asserts/bootstrap/dist/js/bootstrap',
    jquery: '../../asserts/jquery/dist/jquery',
    'jquery-ui': '../../asserts/jquery-ui/jquery-ui',
    bootstraphoverdropdown: '../../asserts/metronic/global/plugins/bootstrap-hover-dropdown/bootstrap-hover-dropdown.min',
    slimscroll: '../../asserts/metronic/global/plugins/jquery-slimscroll/jquery.slimscroll.min',
    metronic: '../../asserts/metronic/global/metronic',
    'angular-bootstrap': '../../asserts/angular-bootstrap/ui-bootstrap-tpls',
    'jquery.blockui': '../../asserts/metronic/global/plugins/jquery.blockui.min',
    'jquery.cokie': '../../asserts/metronic/global/plugins/jquery.cokie.min',
    'jquery.uniform': '../../asserts/metronic/global/plugins/uniform/jquery.uniform.min',
    layout: '../../asserts/metronic/admin/layout/layout',
    ocLazyLoad: '../../asserts/metronic/global/plugins/ocLazyLoad.min',
    'angular-mocks': '../../asserts/angular-mocks/angular-mocks'
  },
  shim: {
    angular: {
      exports: 'angular'
    },
    'angular-cookies': [
      'angular'
    ],
    'angular-sanitize': [
      'angular'
    ],
    'angular-resource': [
      'angular'
    ],
    'angular-animate': [
      'angular'
    ],
    'angular-ui-router': [
      'angular'
    ],
    metronic: {
      deps: [
        'bootstrap',
        'jquery',
        'jquery-ui',
        'bootstraphoverdropdown',
        'slimscroll'
      ],
      exports: 'Metronic'
    },
    layout: {
      deps: [
        'metronic'
      ]
    },
    'angular-bootstrap': [
      'angular',
      'bootstrap'
    ],
    bootstraphoverdropdown: {
      deps: [
        'jquery'
      ]
    },
    bootstrap: {
      deps: [
        'jquery'
      ]
    },
    slimscroll: {
      deps: [
        'jquery'
      ]
    },
    'angular-mocks': {
      deps: [
        'angular'
      ],
      exports: 'angular.mock'
    }
  },
  priority: [
    'angular'
  ],
  packages: [

  ]
});

//http://code.angularjs.org/1.2.1/docs/guide/bootstrap#overview_deferred-bootstrap
window.name = 'NG_DEFER_BOOTSTRAP!';

require([
  'angular',
  'app',
  'angular-cookies',
  'angular-sanitize',
  'angular-resource',
  'angular-animate',
  'angular-ui-router',
  'layout',
  'angular-bootstrap'
], function(angular, app, ngCookies, ngSanitize, ngResource, ngAnimate, uiRouter, layout, bootstrap) {
  'use strict';
  /* jshint ignore:start */
  var $html = angular.element(document.getElementsByTagName('html')[0]);
  /* jshint ignore:end */
  angular.element().ready(function() {
    angular.resumeBootstrap([app.name]);
  });
});

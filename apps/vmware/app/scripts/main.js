/*jshint unused: vars */
require.config({
    paths: {
        angular: '../../bower_components/angular/angular',
        'angular-animate': '../../bower_components/angular-animate/angular-animate',
        'angular-cookies': '../../bower_components/angular-cookies/angular-cookies',
        'angular-mocks': '../../bower_components/angular-mocks/angular-mocks',
        'angular-sanitize': '../../bower_components/angular-sanitize/angular-sanitize',
        bootstrap: '../../bower_components/bootstrap/dist/js/bootstrap',
        'angular-ui-router': '../../bower_components/angular-ui-router/release/angular-ui-router',
        'angular-route': '../../asserts/angular-route/angular-route',
        jquery: '../../bower_components/jquery/dist/jquery',
        'jquery-ui': '../../bower_components/jquery-ui/jquery-ui',
        bootstraphoverdropdown: '../../asserts/metronic/global/plugins/bootstrap-hover-dropdown/bootstrap-hover-dropdown.min',
        slimscroll: '../../asserts/metronic/global/plugins/jquery-slimscroll/jquery.slimscroll.min',
        metronic: '../../asserts/metronic/global/metronic',
        layout: '../../asserts/metronic/admin/layout/layout',
        'angular-resource': '../../bower_components/angular-resource/angular-resource',
        'angular-bootstrap': '../../bower_components/angular-bootstrap/ui-bootstrap-tpls',
        'bootstrap-tpls': '../../asserts/angular-bootstrap/ui-bootstrap-tpls.min',
        highcharts: '../../bower_components/highcharts/highcharts',
        'highcharts-more': '../../bower_components/highcharts/highcharts-more',
        exporting: '../../bower_components/highcharts/modules/exporting'
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
        'angular-animate': [
            'angular'
        ],
        'angular-mocks': {
            deps: [
                'angular'
            ],
            exports: 'angular.mock'
        },
        'angular-ui-router': [
            'angular'
        ],
        'angular-bootstrap': [
            'angular',
            'bootstrap-tpls'
        ],
        'bootstrap-tpls': [
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
        bootstrap: {
            deps: [
                'jquery'
            ]
        },
        bootstraphoverdropdown: {
            deps: [
                'jquery'
            ]
        },
        slimscroll: {
            deps: [
                'jquery'
            ]
        },
        layout: {
            deps: [
                'metronic'
            ]
        },
        jquery: {
            exports: 'jQuery'
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
    'angular-animate',
    'angular-ui-router',
    'layout',
    'angular-bootstrap',
    'highcharts',
], function (angular, app, ngCookies, ngSanitize, ngAnimate, uiRouter, layout, bootstrap) {
    'use strict';
    /* jshint ignore:start */
    var $html = angular.element(document.getElementsByTagName('html')[0]);
    /* jshint ignore:end */
    angular.element().ready(function () {
        angular.resumeBootstrap([app.name]);
    });
});

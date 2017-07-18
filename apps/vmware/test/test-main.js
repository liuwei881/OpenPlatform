var tests = [];
for (var file in window.__karma__.files) {
  if (window.__karma__.files.hasOwnProperty(file)) {
    // Removed "Spec" naming from files
    if (/Spec\.js$/.test(file)) {
      tests.push(file);
    }
  }
}

requirejs.config({
    // Karma serves files from '/base'
    baseUrl: '/base/app/scripts',

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
        'angular' : {'exports' : 'angular'},
        'angular-cookies': ['angular'],
        'angular-sanitize': ['angular'],
        'angular-resource': ['angular'],
        'angular-animate': ['angular'],
        'angular-mocks': {
          deps:['angular'],
          'exports':'angular.mock'
        }
    },

    // ask Require.js to load these files (all our tests)
    deps: tests,

    // start test run, once Require.js is done
    callback: window.__karma__.start
});

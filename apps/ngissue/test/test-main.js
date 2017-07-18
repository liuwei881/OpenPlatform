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
    'angular-mocks': '../../asserts/angular-mocks/angular-mocks',
    highcharts: '../../asserts/highcharts/dist/highcharts-ng'
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

define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name resolutionApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the resolutionApp
     */
    angular.module('resolutionApp.controllers.DashboardCtrl', [])
        .controller('DashboardCtrl', function ($scope, $http) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

            $http.get('/api/v2/getinfo/').success(function (data){
                    if(data.status == 200){
                        Highcharts.chart('recordstatistics', {
                            chart: {
                                type: 'line'
                            },
                            title: {
                                text: 'DNS 记录统计'
                            },
                            subtitle: {
                                text: '数据来源: 操作记录'
                            },
                            xAxis: {
                                categories: data.datetime
                            },
                            yAxis: {
                                title: {
                                    text: '统计值(次)'
                                }
                            },
                            plotOptions: {
                                line: {
                                    dataLabels: {
                                        enabled: true
                                    },
                                    enableMouseTracking: false
                                }
                            },
                            series: data.data
                        });

                    }
                        });
        });
});

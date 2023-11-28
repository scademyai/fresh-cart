// Karma configuration
// Generated on Wed Apr 19 2023 14:54:34 GMT+0000 (Coordinated Universal Time)

module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-spec-reporter'),
      require('karma-chrome-launcher'),
      require('@angular-devkit/build-angular/plugins/karma')
    ],
    files: [
      'src/**/*.spec.ts'
    ],
    reporters: ['spec'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    customLaunchers: {
      ChromeHeadless: {
        base: 'Chrome',
        flags: [
          '--no-sandbox',
          '--disable-gpu',
          '--headless',
          '--remote-debugging-port=9222',
        ],
      },
    },
    browsers: ['ChromeHeadless'],
    singleRun: true,
    restartOnFileChange: true,
  })
}

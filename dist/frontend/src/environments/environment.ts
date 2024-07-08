// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  api: 'http://localhost:8880',
  // socket: "ws://192.168.3.117:8300/",
  socket: "ws://127.0.0.1:8300/",
  enable_auto_reconnect: true,
  allowDanger: true,
  dangerLevel: 95,
  floorAssignments: {
    'ground-floor': 1,
    'first-floor': 2
  }
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.

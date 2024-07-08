const SERVER_IP = "INSTALL_SERVER_IP";
const WEB_PROTOCOL = "http";
const SOCK_PROTOCOL = "ws";

export const environment = {
  production: true,
  api: WEB_PROTOCOL + "://" + SERVER_IP + ":8000",
  socket: SOCK_PROTOCOL + "://" + SERVER_IP + ":8300/",
  enable_auto_reconnect: true,
  allowDanger: false,
  dangerLevel: 95,
  floorAssignments: {
    'ground-floor': 1,
    'first-floor': 2
  }
};

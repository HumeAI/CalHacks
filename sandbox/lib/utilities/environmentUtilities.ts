const ApiUrlHttp = Object.freeze({
  DEV: "http://127.0.0.1:8080",
  TEST: "https://test-api.hume.ai",
  PROD: "https://api.hume.ai",
});

const ApiUrlWs = Object.freeze({
  DEV: "ws://127.0.0.1:8080",
  TEST: "wss://test-api.hume.ai",
  PROD: "wss://api.hume.ai",
});

export enum Environment {
  Dev = "dev",
  Test = "test",
  Prod = "prod",
}

export function parseEnvironment(env: string): Environment {
  switch (env) {
    case "dev":
      return Environment.Dev;
    case "test":
      return Environment.Test;
    case "prod":
      return Environment.Prod;
    default:
      return Environment.Prod;
  }
}

export function getApiUrlHttp(environment: Environment): string {
  switch (environment) {
    case Environment.Dev:
      return ApiUrlHttp.DEV;
    case Environment.Test:
      return ApiUrlHttp.TEST;
    case Environment.Prod:
      return ApiUrlHttp.PROD;
    default:
      return ApiUrlHttp.PROD;
  }
}

export function getApiUrlWs(environment: Environment): string {
  switch (environment) {
    case Environment.Dev:
      return ApiUrlWs.DEV;
    case Environment.Test:
      return ApiUrlWs.TEST;
    case Environment.Prod:
      return ApiUrlWs.PROD;
    default:
      return ApiUrlWs.PROD;
  }
}

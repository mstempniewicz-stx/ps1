import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

export interface Callbacks {
  onUnauthorized: () => Promise<unknown>;
  onInvalidTokens: () => Promise<unknown>;
}

interface RequestConfig extends AxiosRequestConfig {
  _skipErrorHandler?: boolean;
}

export class RestClient {
  private readonly fetcher: AxiosInstance;
  private readonly defaultConfig = { method: 'GET' };
  private callbacks: Callbacks = {
    onInvalidTokens: Promise.resolve,
    onUnauthorized: Promise.resolve,
  };

  constructor(apiUrl = '') {
    this.fetcher = axios.create({
      baseURL: apiUrl,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.addErrorHandler();
  }

  private get authHeader() {
    return this.fetcher.defaults.headers.common.Authorization;
  }

  private set authHeader(header) {
    this.fetcher.defaults.headers.common.Authorization = header;
  }

  request(url: string, config: RequestConfig = {}) {
    const conf = stripUndefined({ url, ...this.defaultConfig, ...config }) as AxiosRequestConfig;

    return this.fetcher(conf);
  }

  setAuthHeader(header?: string) {
    delete this.fetcher.defaults.headers.common.Authorization;
    if (header) {
      this.authHeader = header;
    }
  }

  updateErrorHandles(callbacks: Callbacks) {
    this.callbacks = callbacks;
  }

  private addErrorHandler() {
    this.fetcher.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (err: any) => {
        const originalRequest = err.config as RequestConfig;
        if (err.response.status === 401 && this.authHeader && !originalRequest._skipErrorHandler) {
          originalRequest._skipErrorHandler = true;
          try {
            await this.callbacks.onUnauthorized();
          } catch (e) {
            if (this.authHeader) {
              await this.callbacks.onInvalidTokens();
            }
          }

          if (this.authHeader) {
            delete originalRequest.headers.Authorization;
            return this.fetcher(originalRequest);
          }
        }

        return Promise.reject(err);
      }
    );
  }
}

function stripUndefined<T>(data: T): T {
  return JSON.parse(JSON.stringify(data));
}

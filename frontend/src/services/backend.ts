import { LoginData, SignUpData, User } from '../backendTypes';
import { RestClient } from './utils/restClient';

class Backend {
  private readonly http: RestClient;
  private readonly tokenStorage = new TokenStorage();
  private invalidTokensListeners: Array<() => Promise<void>> = [];

  constructor(apiUrl: string = '/api/v1') {
    this.http = new RestClient(apiUrl);
    this.http.updateErrorHandles({
      onUnauthorized: () => this.refreshTokens(),
      onInvalidTokens: () => {
        this.clearCredentials();
        return Promise.all(this.invalidTokensListeners.map(cb => cb()));
      },
    });

    const access = this.tokenStorage.access;
    if (access) {
      this.http.setAuthHeader(`Bearer ${access}`);
    }
  }

  listenOnInvalidTokens(cb: () => Promise<void>) {
    this.invalidTokensListeners.push(cb);
  }

  async login(credentials: LoginData) {
    return this.http
      .request('/token/', {
        method: 'POST',
        data: credentials,
      })
      .then(({ data }) => this.setTokens(data));
  }

  async signUp(data: SignUpData) {
    return this.http.request('/accounts/register/', {
      method: 'POST',
      data,
    });
  }

  async getCurrentUser(): Promise<User> {
    if (this.tokenStorage.refresh) {
      const { data } = await this.http.request('/accounts/me/');
      return data;
    } else {
      throw new Error('No tokens to get the user with');
    }
  }

  private async refreshTokens(): Promise<void> {
    const {
      data: { access, refresh },
    } = await this.http.request('/token/refresh/', {
      method: 'POST',
      data: { refresh: this.tokenStorage.refresh },
      _skipErrorHandler: true,
    });

    this.setTokens({ access, refresh });
  }

  clearCredentials() {
    this.setTokens({ access: null, refresh: null });
  }

  private setTokens({ access, refresh }: { access: string | null; refresh: string | null }) {
    if (access) {
      this.http.setAuthHeader(`Bearer ${access}`);
    }
    this.tokenStorage.access = access;
    this.tokenStorage.refresh = refresh;
  }
}

class TokenStorage {
  get access() {
    return window.localStorage.getItem('auth:accessToken');
  }

  set access(access) {
    if (access) {
      window.localStorage.setItem('auth:accessToken', access);
    } else {
      window.localStorage.removeItem('auth:accessToken');
    }
  }

  get refresh() {
    return window.localStorage.getItem('auth:refreshToken');
  }

  set refresh(refresh) {
    if (refresh) {
      window.localStorage.setItem('auth:refreshToken', refresh);
    } else {
      window.localStorage.removeItem('auth:refreshToken');
    }
  }
}

export const backend = new Backend(process.env.REACT_APP_BACKEND_URL || '/api/v1');

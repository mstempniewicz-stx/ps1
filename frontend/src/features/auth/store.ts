import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { routerActions } from 'connected-react-router';
import { channel } from 'redux-saga';
import { fork, put, takeEvery, takeLeading } from 'redux-saga/effects';

import { LoginData, SignUpData, User } from '../../backendTypes';
import { backend } from '../../services/backend';

interface AuthState {
  pending: boolean;
  errors?: Record<string, string>;
  user?: User;
}

const initialState: AuthState = {
  pending: true,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loadUser(state, { payload }: PayloadAction<{ user?: User }>) {
      state.pending = false;
      state.user = payload.user;
    },
    login(state, action: PayloadAction<LoginData>) {
      state.pending = true;
    },
    loginSuccess(state, { payload }: PayloadAction<{ user: User }>) {
      state.pending = false;
      state.user = payload.user;
    },
    loginFailure(state, { payload }: PayloadAction<{ errors: Record<string, string> }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
    signUp(state, action: PayloadAction<SignUpData>) {
      state.pending = true;
    },
    signUpSuccess(state) {
      state.pending = false;
    },
    signUpFailure(state, { payload }: PayloadAction<{ errors: Record<string, string> }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
    logout() {},
  },
});

export const authActions = authSlice.actions;

function* loginSaga() {
  try {
    const { user } = yield backend.getCurrentUser();
    yield put(authActions.loadUser({ user }));
  } catch {
    yield put(authActions.loadUser({ user: undefined }));
  }

  yield takeLeading(authActions.login, function* ({ payload }) {
    try {
      yield backend.login(payload);
      const { user } = yield backend.getCurrentUser();
      yield put(authActions.loginSuccess({ user }));
      yield put(routerActions.push('/authenticated'));
    } catch (e) {
      const errors = e.response.data;
      yield put(authActions.loginFailure({ errors }));
    }
  });
}

function* signUpSaga() {
  yield takeLeading(authActions.signUp, function* ({ payload }) {
    try {
      yield backend.signUp(payload);
      yield put(authActions.signUpSuccess());
      yield put(authActions.login(payload));
    } catch (e) {
      const errors = e.response.data;
      yield put(authActions.signUpFailure({ errors }));
    }
  });
}

export function* logoutSaga() {
  const badTokenChannel = channel<any>();
  backend.listenOnInvalidTokens(async () => badTokenChannel.put(''));
  yield takeEvery(badTokenChannel, function* () {
    yield put(authActions.logout());
  });

  yield takeLeading(authActions.logout, function* () {
    backend.clearCredentials();
    window.location.assign('/');
  });
}

export function* authSaga() {
  yield fork(loginSaga);
  yield fork(logoutSaga);
  yield fork(signUpSaga);
}

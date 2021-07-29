import { configureStore } from '@reduxjs/toolkit';
import { connectRouter, routerMiddleware } from 'connected-react-router';
import { History } from 'history';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import createSagaMiddleware from 'redux-saga';

import { authSaga, authSlice } from '../features/auth/store';

export const createStore = (history: History) => {
  const saga = createSagaMiddleware();

  const store = configureStore({
    reducer: {
      router: connectRouter(history) as any,
      [authSlice.name]: authSlice.reducer,
    },
    middleware: getDefaultMiddleware =>
      getDefaultMiddleware({ thunk: false }).concat(saga).concat(routerMiddleware(history)),
  });

  saga.run(authSaga);

  return store;
};
type StoreType = ReturnType<typeof createStore>;

export type State = ReturnType<StoreType['getState']>;
export const useAppDispatch = () => useDispatch<StoreType['dispatch']>();
export const useAppSelector: TypedUseSelectorHook<State> = useSelector;

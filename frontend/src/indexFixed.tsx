import './i18n';

import { ConnectedRouter as Router } from 'connected-react-router';
import { createBrowserHistory } from 'history';
import React from 'react';
import { Provider as ReduxProvider } from 'react-redux';

import App from './App';
import { createStore } from './services/store';

const history = createBrowserHistory();
const store = createStore(history);

/**
 * TODO: Move contents of this file to index.tsx
 * This file exists because of the issue CRA 4 has with React Fast Refresh
 * https://github.com/facebook/create-react-app/issues/9984
 * But this shouldn't be defined in App.tsx as those providers
 * would be replaced in different envs (i.e. SSR)
 */
export const AppIndex = () => (
  <React.StrictMode>
    <ReduxProvider store={store}>
      <Router history={history}>
        <App />
      </Router>
    </ReduxProvider>
  </React.StrictMode>
);

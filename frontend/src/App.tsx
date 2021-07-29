import './index.css';

import { Switch } from 'react-router-dom';

import { LazyPages } from './features/lazy';
import { useAppSelector } from './services/store';
import { AnonymousLayout } from './ui-components/layouts/AnonymousLayout';
import { AuthLayout } from './ui-components/layouts/AuthLayout';
import { DashboardLayout } from './ui-components/layouts/DashboardLayout';
import { EnhancedRoute, RouteDefinition } from './ui-components/Routing';

const routeDefaults: RouteDefinition = {
  exact: true,
  requiresAuth: true,
  layout: AnonymousLayout,
  content: () => <></>,
  path: '/',
};

const route404: RouteDefinition = {
  ...routeDefaults,
  path: '*',
  layout: AnonymousLayout,
  content: () => <>404</>,
};

const routes: Partial<RouteDefinition>[] = [
  { path: '/', requiresAuth: false, layout: AnonymousLayout, content: LazyPages.HomePage },
  {
    path: '/authenticated',
    requiresAuth: true,
    layout: DashboardLayout,
    content: LazyPages.AuthenticatedPage,
  },
  {
    path: '/login',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.LoginPage,
  },
  {
    path: '/register',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.RegisterPage,
  },
  {
    path: '/reset-password',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.ResetPasswordPage,
  },
  route404,
];

function App() {
  const isAuthenticated = useAppSelector(state => !!state.auth.user);
  const isAuthPending = useAppSelector(state => state.auth.pending);

  return (
    <Switch>
      {routes
        .map(route => ({ ...routeDefaults, ...route }))
        .map((route, i) => (
          <EnhancedRoute
            key={i}
            exact={route.exact}
            path={route.path}
            route={route}
            isAuthenticated={isAuthenticated}
            isAuthPending={isAuthPending}
            authFallbackRoute={route404}
          />
        ))}
    </Switch>
  );
}

export default App;

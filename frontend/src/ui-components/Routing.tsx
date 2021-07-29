import { Suspense } from 'react';
import { RouteProps } from 'react-router';
import { Route } from 'react-router-dom';

import { AppLoader } from './AppLoader';

export interface RouteDefinition {
  path: string;
  exact?: boolean;
  requiresAuth?: boolean;
  layout: React.ComponentType<{ children: React.ReactNode }>;
  content: React.ComponentType;
  layoutProps?: Object;
}

interface EnhancedRouteProps {
  route: RouteDefinition;
  authFallbackRoute: RouteDefinition;
  isAuthenticated: boolean;
  isAuthPending: boolean;
}

export const EnhancedRoute = ({
  route,
  isAuthPending,
  isAuthenticated,
  authFallbackRoute,
  ...rest
}: RouteProps & EnhancedRouteProps) => {
  let { layout: Layout, content: Content, requiresAuth, layoutProps } = route;

  if (isAuthPending && requiresAuth) {
    return <AppLoader />;
  }

  if (requiresAuth && !isAuthenticated) {
    Layout = authFallbackRoute.layout;
    Content = authFallbackRoute.content;
    layoutProps = {};
  }

  return (
    <Route
      {...rest}
      render={() => (
        <Layout {...layoutProps}>
          <Suspense fallback={''}>
            <Content />
          </Suspense>
        </Layout>
      )}
    />
  );
};

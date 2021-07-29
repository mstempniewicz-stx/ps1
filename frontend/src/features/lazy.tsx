import { lazy } from 'react';

import { namedImportToDefault } from '../services/imports';

const Pages = {
  HomePage: () => import('./homepage/HomePage'),
  AuthenticatedPage: () => import('./auth/AuthenticatedPage'),
  RegisterPage: () => import('./auth/RegisterPage'),
  LoginPage: () => import('./auth/LoginPage'),
  ResetPasswordPage: () => import('./auth/ResetPasswordPage'),
};

export const LazyPages = Object.fromEntries(
  Object.entries(Pages).map(([name, importFn]) => [
    name,
    lazy(namedImportToDefault(importFn, name)),
  ])
);

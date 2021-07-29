import { Formik } from 'formik';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';

import { FormikInput } from '../../ui-components/Input';
import { Title } from '../../ui-components/Typography';
import { Button, Form, Link } from './common';
import { authActions } from './store';
import { getRegisterSchema } from './validation';

export const RegisterPage = () => {
  const dispatch = useDispatch();
  const { signUp } = authActions;
  const { t } = useTranslation();

  return (
    <Formik
      initialValues={{ email: '', password: '', repeatPassword: '', firstName: '', lastName: '' }}
      onSubmit={async values => dispatch(signUp(values))}
      validationSchema={getRegisterSchema()}
    >
      {({ values, handleSubmit }) => (
        <Form onSubmit={handleSubmit}>
          <Title>
            {t('auth.getStarted')}
            <br />
            {t('auth.withFreeAccount')}
          </Title>
          <FormikInput
            type="text"
            name="firstName"
            label="first name"
            placeholder={t('auth.firstName')}
            value={values.firstName}
          />
          <FormikInput
            type="text"
            name="lastName"
            label="last name"
            placeholder={t('auth.lastName')}
            value={values.lastName}
          />
          <FormikInput
            type="email"
            name="email"
            label="email"
            placeholder={t('auth.email')}
            value={values.email}
          />
          <FormikInput
            type="password"
            name="password"
            label="password"
            placeholder={t('auth.password')}
            value={values.password}
          />
          <FormikInput
            type="password"
            name="repeatPassword"
            label="Re-type password"
            placeholder="Re-type password"
            value={values.repeatPassword}
          />
          <Button type="submit">{t('auth.getStarted')}</Button>
          <Link to="/login">{t('auth.loginLink')}</Link>
        </Form>
      )}
    </Formik>
  );
};

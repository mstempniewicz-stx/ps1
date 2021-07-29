import styled from '@emotion/styled';
import { Formik } from 'formik';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';

import { FormikInput } from '../../ui-components/Input';
import { Link, Title } from '../../ui-components/Typography';
import { Button, Form } from './common';
import { authActions } from './store';

export const LoginPage = () => {
  const dispatch = useDispatch();
  const { login } = authActions;
  const { t } = useTranslation();

  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      onSubmit={async values => dispatch(login(values))}
    >
      {({ values, handleSubmit }) => (
        <Form onSubmit={handleSubmit}>
          <Title>{t('auth.loginTitle')}</Title>
          <FormikInput
            type="text"
            name="email"
            label="email"
            placeholder={t('auth.email')}
            value={values.email}
            required
          />
          <FormikInput
            type="password"
            name="password"
            label="password"
            placeholder={t('auth.password')}
            value={values.password}
            required
          />
          <Button type="submit">{t('auth.loginButton')}</Button>
          <LinksContainer>
            <Link to="/register">{t('auth.registerLink')}</Link>
            <StyledLink to="/reset-password">{t('auth.forgotLink')}</StyledLink>
          </LinksContainer>
        </Form>
      )}
    </Formik>
  );
};

const LinksContainer = styled.div`
  margin-top: 1.875rem;
  display: flex;
  flex-direction: column;
`;

const StyledLink = styled(Link)`
  margin-top: 0.3rem;
`;

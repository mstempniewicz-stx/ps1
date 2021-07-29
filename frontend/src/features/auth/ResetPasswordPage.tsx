import { Formik } from 'formik';
import { useTranslation } from 'react-i18next';

import { FormikInput } from '../../ui-components/Input';
import { Title } from '../../ui-components/Typography';
import { Button, Form, Link } from './common';

export const ResetPasswordPage = () => {
  const { t } = useTranslation();
  return (
    <Formik
      initialValues={{ email: '' }}
      onSubmit={values => {
        console.log(values);
      }}
    >
      {({ values, handleSubmit }) => (
        <Form onSubmit={handleSubmit}>
          <Title>{t('auth.resetPasswordTitle')}</Title>
          <FormikInput
            type="text"
            name="email"
            label="email"
            placeholder={t('auth.email')}
            value={values.email}
            required
          />
          <Button type="submit">Send email</Button>
          <Link to="/login">Return to login</Link>
        </Form>
      )}
    </Formik>
  );
};

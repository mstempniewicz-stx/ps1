import * as Yup from 'yup';

import { t } from '../../i18n';

export const getRegisterSchema = () =>
  Yup.object().shape({
    email: Yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: Yup.string()
      .required(t('validation.required'))
      .min(8, t('validation.minPassword', { min: '8' })),
    repeatPassword: Yup.string()
      .oneOf([Yup.ref('password'), null], t(`validation.passwordMatch`))
      .required(t('validation.required')),
    firstName: Yup.string().required(t('validation.required')),
    lastName: Yup.string().required(t('validation.required')),
  });

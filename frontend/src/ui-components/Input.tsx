import styled from '@emotion/styled';
import { useField } from 'formik';
import { FC, InputHTMLAttributes, useState } from 'react';

import showPassword from '../assets/icons/show-password.svg';
import { FormError } from './Typography';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  name: string;
  label: string;
  invalid?: string;
  error?: string;
}

interface FormikInputProps extends InputHTMLAttributes<HTMLInputElement> {
  name: string;
  label: string;
}

export const FormikInput: FC<FormikInputProps> = ({ type, name, label, ...rest }): any => {
  const [field, meta, { setValue, setTouched }] = useField({ name, type, ...rest });
  const invalid = meta.touched ? meta.error : undefined;

  return (
    <Input
      type={type}
      name={name}
      value={field.value}
      onChange={e => setValue(e.target.value)}
      onBlur={() => setTouched(true)}
      label={label}
      error={meta.error}
      invalid={invalid}
      {...rest}
    />
  );
};

export const Input: FC<InputProps> = ({ type, name, label, invalid, error, ...rest }) => {
  const [passwordVisible, setPasswordVisibility] = useState(false);

  const handlePasswordVisibility = () => {
    setPasswordVisibility(prevState => !prevState);
  };

  return (
    <Label>
      <StyledInput
        type={passwordVisible ? 'text' : type}
        name={name}
        aria-label={label}
        {...rest}
      />
      {type === 'password' && <PasswordIcon onClick={handlePasswordVisibility} />}
      {invalid && <FormError>{error}</FormError>}
    </Label>
  );
};

const Label = styled.label`
  width: 100%;
  position: relative;
  margin-bottom: 1.5rem;
`;

const StyledInput = styled.input`
  width: 100%;
  border-radius: var(--border-radius);
  border: var(--border-input);
  padding: 0.625rem;
  font-size: var(--font-size-m);
`;

const PasswordIcon = styled.div`
  position: absolute;
  top: 0.625rem;
  right: 0.625rem;
  width: 1.25rem;
  height: 1.25rem;
  background-image: url(${showPassword});
  background-repeat: no-repeat;
  background-size: cover;
  cursor: pointer;
`;

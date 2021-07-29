import styled from '@emotion/styled';
import { Link as BaseLink } from 'react-router-dom';

export const Title = styled.h1`
  font-size: var(--font-size-xl);
  text-align: center;
  color: var(--color-font);
`;

export const Link = styled(BaseLink)`
  font-size: var(--font-size-s);
  color: var(--color-main);
  text-decoration: none;
`;

export const FormError = styled.p`
  margin: 3px 0 0 0;
  color: var(--color-error);
  font-size: var(--font-size-s);
`;

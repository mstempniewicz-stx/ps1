import styled from '@emotion/styled';

import { Button as BaseButton } from '../../../ui-components/Button';
import { Link as BaseLink } from '../../../ui-components/Typography';

export const Button = styled(BaseButton)`
  width: 100%;
`;

export const Link = styled(BaseLink)`
  margin-top: 1.875rem;
`;

export const Form = styled.form`
  width: 25rem;
  display: flex;
  flex-direction: column;

  @media (max-width: 480px) {
    width: 90%;
  }
`;

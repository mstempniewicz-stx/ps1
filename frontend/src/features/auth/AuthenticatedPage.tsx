import styled from '@emotion/styled';

import { Title } from '../../ui-components/Typography';

export const AuthenticatedPage = () => {
  return (
    <Container>
      <Title>This is an authenticated route</Title>
    </Container>
  );
};

const Container = styled.div`
  display: grid;
  place-items: center;
  height: 100%;
`;

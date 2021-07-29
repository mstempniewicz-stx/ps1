import styled from '@emotion/styled';
import { ReactNode } from 'react';

import heroIcon from '../../assets/icons/hero-icon.svg';
import { Logo } from '../Icons';
interface Props {
  children: ReactNode;
}

export const AuthLayout = ({ children }: Props) => {
  return (
    <Container>
      <HeroImage>
        <Hero />
      </HeroImage>
      <FormSection>
        <Logo />
        {children}
      </FormSection>
    </Container>
  );
};

const Container = styled.main`
  display: grid;
  min-height: 100vh;
  grid-template-columns: 1fr 1fr;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const HeroImage = styled.div`
  display: grid;
  place-items: center;
  background: var(--color-auth-background);

  @media (max-width: 1024px) {
    display: none;
  }
`;

const FormSection = styled.section`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Hero = styled.div`
  width: 31.25rem;
  height: 31.25rem;
  margin-right: 1.875rem;
  background-image: url(${heroIcon});
  background-repeat: no-repeat;
  background-size: 100% 100%;
`;

import styled from '@emotion/styled';
import { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

import heroIcon from '../../assets/icons/hero-icon.svg';
import { Button as BaseButton } from '../Button';
import { Logo } from '../Icons';
interface Props {
  children: ReactNode;
}

export const AnonymousLayout = ({ children }: Props) => {
  const { t } = useTranslation();
  return (
    <Container>
      <HeroImage>
        <Hero />
      </HeroImage>
      <Section>
        <Logo />
        {children}
        <LogInSection>
          {t('auth.loginTitle')}:
          <Link to="/login">
            <Button>{t('auth.loginButton')}</Button>
          </Link>
        </LogInSection>
      </Section>
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

const Button = styled(BaseButton)`
  width: 25rem;
`;

const LogInSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  height: 4rem;
  margin-top: 3rem;
`;

const Section = styled.section`
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

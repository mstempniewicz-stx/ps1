import styled from '@emotion/styled';
import { ReactNode } from 'react';
import { useDispatch } from 'react-redux';

import { authActions } from '../../features/auth/store';
import { Button } from '../Button';
import { Logo as BaseLogo } from '../Icons';

interface Props {
  children: ReactNode;
}

export const DashboardLayout = ({ children }: Props) => {
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(authActions.logout());
  };

  return (
    <>
      <Header>
        <Logo />
        <LogoutButton onClick={handleLogout}>Log out</LogoutButton>
      </Header>
      <Content>{children}</Content>
      <Footer />
    </>
  );
};

const Header = styled.header`
  height: 4rem;
  background: var(--color-main);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const Content = styled.main`
  height: calc(100vh - 7rem);
`;

const Footer = styled.footer`
  height: 3rem;
  background: var(--color-main);
`;

const Logo = styled(BaseLogo)`
  margin-left: 2rem;
`;

const LogoutButton = styled(Button)`
  margin-right: 2rem;
  border: 1px solid var(--color-button-border);

  &:hover {
    background: var(--color-main-brighter);
  }
`;
